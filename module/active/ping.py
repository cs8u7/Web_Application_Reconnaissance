import subprocess
import ipaddress
import dns.resolver
import os
import re

current_ip = 0

def ping_sweep(ip, folder_sample):
    global current_ip 
    ip_net = ipaddress.ip_network(ip, strict=False)
    live_hosts = []

    for ip in ip_net.hosts():
        current_ip += 1
        print(f"[{(current_ip/256)*100:.2f}%][{current_ip}/256]", end='\r')
        ip = str(ip)
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                ttl_match = re.search(
                    r'ttl=(\d+)', result.stdout.decode('utf-8'))
                if ttl_match:
                    if detect_os(int(ttl_match.group(1))) == 1:
                        live_hosts.append(f'{ip}#Linux')
                    elif detect_os(int(ttl_match.group(1))) == 2:
                        live_hosts.append(f'{ip}#Window')
                    elif detect_os(int(ttl_match.group(1))) == 0:
                        live_hosts.append(f'{ip}#Undetected')

            with open(f'{folder_sample}/active/alive_ip.txt', 'w') as file:
                for ip in live_hosts:
                    file.write(f'{ip}\n')
        except Exception:
            pass


def ip_to_cidr(ip):
    network = ipaddress.IPv4Network(f'{ip}/24', strict=False)
    return str(network)


def detect_os(ttl):
    if ttl:
        if ttl > 100:
            original_ttl = 128
        elif ttl > 200:
            original_ttl = 255
        else:
            original_ttl = 64

        if original_ttl == 64:
            return 1
        elif original_ttl == 128:
            return 2
        elif original_ttl == 255:
            return 0
    else:
        return 0


def dns_ip_query(domain):
    resolver = dns.resolver.Resolver()
    IPs = []
    isp_set = ['8.8.8.8', '1.1.1.1', '1.0.0.1']
    for isp in isp_set:
        try:
            resolver.nameservers = [isp]
            response = resolver.resolve(domain, 'A')
            for data in response:
                IPs.append(str(data))
        except Exception:
            return sorted(set(IPs))
    return sorted(set(IPs))


def ping(domain, folder_sample):
    ipv4_sample = folder_sample + '/passive/ipv4.txt'
    if not os.path.exists(ipv4_sample):
        ip_lines = dns_ip_query(domain)
    else:
        with open(ipv4_sample, 'r') as file:
            ip_lines = file.readlines()

    for ip in ip_lines:
        ping_sweep(ip_to_cidr(ip), folder_sample)

