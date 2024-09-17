import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import concurrent.futures
from module.active.ping import dns_ip_query
import os
import time


lock = Lock()
progress_lock = Lock()
progress = 0

SOCKET_TIMEOUT = 20


def banner_collector(port, ip, banner_sample, total_tasks):
    global progress
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            s.connect((ip, int(port)))
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    result = f"port {port}:\n {banner}"
                    with open(f'{banner_sample}{ip}.txt', 'a') as file:
                        file.write(f'{result}\n')
            except socket.timeout:
                pass
            except Exception:
                pass

    except socket.timeout:
        pass
    except Exception:
        pass

    with progress_lock:
        progress += 1
        print(
            f"[{(progress / total_tasks) * 100:.2f}%][{progress}/{total_tasks}]", end='\r')


def banner_grabbing(domain, threads, folder_sample, is_full_range):
    start_time = time.time()
    banner_sample = folder_sample + f'/active/banner_grabbing#'
    port_sample = folder_sample + f'/active/open_port.txt'
    ipv4_sample = folder_sample + '/passive/ipv4.txt'
    ip_lines = []
    if os.path.exists(ipv4_sample):
        with open(ipv4_sample, 'r') as file:
            ip_lines += file.readlines()

    ip_lines += dns_ip_query(domain)
    ip_lines = sorted(set(ip_lines))

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


    for ip in ip_lines:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(
                banner_collector, port.strip(), ip.strip(), banner_sample, total_tasks) for port in ports]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception:
                    pass

    end_time = time.time()
    running = end_time - start_time 
    print(f"\n[Time]: {running:.2f}s")
