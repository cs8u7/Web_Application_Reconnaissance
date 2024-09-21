import subprocess
import dns.resolver
import time
import re


def ping_ttl(domain, IP_OS_sample, unique_IPs):
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            ttl_match = re.search(
                r'ttl=(\d+)', result.stdout.decode('utf-8'))
            ip_match = re.search(
                r'from\s+([\d\.]+)', result.stdout.decode('utf-8'))

            if ttl_match and ip_match:
                detected_ip = ip_match.group(1)
                unique_IPs.append(detected_ip)
                if detect_os(int(ttl_match.group(1))) == 1:
                    with open(IP_OS_sample, 'a') as file:
                        file.write(
                            f'Resolved {domain} to IP {detected_ip}: , OS detected: Linux\n')
                elif detect_os(int(ttl_match.group(1))) == 2:
                    with open(IP_OS_sample, 'a') as file:
                        file.write(
                            f'Resolved {domain} to IP {detected_ip}, OS detected: Window\n')
                elif detect_os(int(ttl_match.group(1))) == 0:
                    with open(IP_OS_sample, 'a') as file:
                        file.write(
                            f'Resolved {domain} to IP {detected_ip}, OS detected: Unknow\n')
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
    start_time = time.time()
    domain_sample = folder_sample + '/active/subdomain.txt'
    IP_OS_sample = folder_sample + '/active/IP_OS.txt'
    unique_IPs_sample = folder_sample + '/active/unique_IPs.txt'

    with open(domain_sample, 'r') as file:
        domains = file.read().splitlines()

    unique_IPs = []

    for domain in domains:
        ping_ttl(domain, IP_OS_sample, unique_IPs)

    unique_IPs = list(set(unique_IPs))

    domain_count = 0
    domain_range = len(domains)
    for ip in unique_IPs:
        domain_count += 1
        print(
                f"[{(domain_count / domain_range) * 100:.2f}%][{domain_count}/{domain_range}]", end='\r')
        with open(unique_IPs_sample, 'a') as file:
            file.write(f'{ip}\n')

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
