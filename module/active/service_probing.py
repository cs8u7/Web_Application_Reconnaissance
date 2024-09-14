import nmap
import concurrent.futures
import os
from threading import Lock
from module.active.ping import dns_ip_query

lock = Lock()
progress_lock = Lock()
progress = 0


def identify_service(ip, port):
    scanner = nmap.PortScanner()
    results = scanner.scan(ip, arguments=f'-sV -p {port} -T4')
    return results


def scan_service_port(ip, port, service_on_port_sample, total_tasks):
    global progress
    try:
        service = identify_service(ip, port)
        with lock:
            with open(f'{service_on_port_sample}{ip}.txt', 'a') as file:
                if service["scan"][ip]["tcp"][int(port)]["name"] != 'unknown':
                    file.write(f'port: {port} status: {service["scan"][ip]["tcp"][int(port)]["state"]}   '
                               f'service: {service["scan"][ip]["tcp"][int(port)]["name"]} '
                               f'method: {service["scan"][ip]["tcp"][int(port)]["reason"]}\n')
                else:
                    pass
    except Exception:
        pass

    with progress_lock:
        progress += 1
        print(
            f"[{(progress / total_tasks) * 100:.2f}%][{progress}/{total_tasks}]", end='\r')


def service_probing(domain, threads, folder_sample, is_full_range):
    ipv4_sample = folder_sample + '/passive/ipv4.txt'
    ip_lines = []
    if os.path.exists(ipv4_sample):
        with open(ipv4_sample, 'r') as file:
            ip_lines += file.readlines()
    ip_lines += dns_ip_query(domain)
    ip_lines = sorted(set(ip_lines))

    service_on_port_sample = folder_sample + f'/active/service_on_port#'
    port_sample = folder_sample + f'/active/open_port.txt'

    ports = []
    with open(port_sample, 'r') as file:
        open_port_lists = [port.strip() for port in file.readlines()]

    if not is_full_range:
        with open('module/active/word_list/default_port.txt', 'r') as file:
            only_scan_port_sample = file.read().splitlines()
        ports = []
        for port in only_scan_port_sample:
            if port in open_port_lists:
                ports.append(port)
    else:
        port = open_port_lists

    total_tasks = len(ip_lines) * len(ports)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for ip in ip_lines:
            for port in ports:
                futures.append(executor.submit(scan_service_port, ip,
                               port, service_on_port_sample, total_tasks))

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception:
                pass

    print(f"", end='\r', flush=True)
