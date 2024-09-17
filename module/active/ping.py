import subprocess
import ipaddress
import dns.resolver
import os
import re


def ping_ttl(ip):
    ip = str(ip)
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            ttl_match = re.search(
                r'ttl=(\d+)', result.stdout.decode('utf-8'))
            if ttl_match:
                if detect_os(int(ttl_match.group(1))) == 1:
                    print(f'[Notification] {ip} is active, OS detected: Linux')
                elif detect_os(int(ttl_match.group(1))) == 2:
                    print(f'[Notification] {ip} is active, OS detected: Window')
                elif detect_os(int(ttl_match.group(1))) == 0:
                    print(f'[Notification] {ip} is active, OS detected: Unknow')
    except Exception:
        pass  

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
    ip_lines = []
    if os.path.exists(ipv4_sample):
        with open(ipv4_sample, 'r') as file:
            ip_lines += file.readlines()

    ip_lines += dns_ip_query(domain)
    ip_lines = sorted(set(ip_lines))

    if len(ip_lines) == 0:
        return True
    else:
        for ip in ip_lines:
            ping_ttl(ip)
        return False
