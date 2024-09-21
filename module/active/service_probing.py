import nmap
import concurrent.futures
from threading import Lock
import time

lock = Lock()
progress_lock = Lock()


def identify_service(ip, port):
    scanner = nmap.PortScanner()
    results = scanner.scan(ip, arguments=f'-sV -p {port} -T4')
    return results


def scan_service_port(ip, port, service_on_port_sample, port_range, current_progress):
    try:
        service = identify_service(ip, port)
        with lock:
            with open(f'{service_on_port_sample}{ip}.txt', 'a') as file:
                if service["scan"][ip]["tcp"][int(port)]["name"] != 'unknown':
                    file.write(f'port: {port} status: {service["scan"][ip]["tcp"][int(port)]["state"]}   '
                               f'service: {service["scan"][ip]["tcp"][int(port)]["name"]} '
                               f'method: {service["scan"][ip]["tcp"][int(port)]["reason"]}\n')
    except Exception:
        pass

    with progress_lock:
        current_progress[0] += 1
        print(
            f"[{(current_progress[0] / port_range) * 100:.2f}%][{current_progress[0]}/{port_range}]", end='\r')


def multi_threaded_service_probe(ip, open_port_lists, threads, service_on_port_sample):
    current_progress = [0]
    port_range = len(open_port_lists)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scan_service_port, ip, port,
                            service_on_port_sample, port_range, current_progress)
            for port in open_port_lists
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def service_probing(threads, folder_sample):
    start_time = time.time()
    unique_IPs_sample = folder_sample + '/active/unique_IPs.txt'
    with open(unique_IPs_sample, 'r') as file:
        IPs = file.read().splitlines()

    service_on_port_sample = folder_sample + f'/active/service_on_port#'
    port_sample = folder_sample + f'/active/open_port.txt'

    with open(port_sample, 'r') as file:
        open_port_lists = [port.strip() for port in file.readlines()]

    for ip in IPs:
        print(f'[-] Service Probing On IP {ip}')
        multi_threaded_service_probe(
            ip, open_port_lists, threads, service_on_port_sample)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
