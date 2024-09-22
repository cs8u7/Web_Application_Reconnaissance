import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import re

port_lock = threading.Lock()
progress_lock = threading.Lock()


def filter_service(service):
    clean_service = re.sub(r'[^\x20-\x7E]+', '', service)
    
    if not clean_service.strip():
        clean_service = "unknown"
    
    return clean_service

def scan_port(port, total_ports, ip, port_sample, current_count):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2) 
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, 'tcp')
                    if service != '# Local services\n':
                        service = filter_service(service)
                        with port_lock:
                            with open(f'{port_sample}{ip}.txt', 'a', encoding='utf-8') as file:
                                file.write(f'port: {port} open {service}\n')
                                banner = s.recv(1024).decode().strip()
                                if banner:
                                    file.write(f'   banner: {banner}\n')
                except OSError:
                    pass

        with progress_lock:
            current_count[0] += 1
            print(
                f"[{(current_count[0] / total_ports) * 100:.2f}%] [{current_count[0]}/{total_ports}]",
                end='\r'
            )

    except Exception as e:
        pass


def multi_threaded_port_scan(threads, port_range, ip, port_sample):
    total_ports = port_range[1] - port_range[0] + 1
    ports = range(port_range[0], port_range[1] + 1)
    current_count = [0]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(
            scan_port, port, total_ports, ip, port_sample, current_count) for port in ports]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                pass


def port_scanning(threads, folder_sample, port_start, port_end):
    start_time = time.time()
    port_sample = folder_sample + f'/active/service_on_open_port#'
    port_range = (port_start, port_end)

    unique_IPs_sample = folder_sample + '/active/unique_IPs.txt'

    with open(unique_IPs_sample, 'r') as file:
        IPs = file.read().splitlines()

    for ip in IPs:
        print(f'[-] Port Scanning On IP {ip}')
        multi_threaded_port_scan(threads, port_range, ip, port_sample)

    end_time = time.time()
    running_time = end_time - start_time
    print(f"\n[Time]: {running_time:.2f}s")
