import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time

lock = Lock()
progress_lock = Lock()
SOCKET_TIMEOUT = 10


def banner_collector(port, ip, banner_sample, port_range, current_progress):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            s.connect((ip, int(port)))
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    result = f"port {port}:\n {banner}"
                    with lock:
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
        current_progress[0] += 1
        print(f"[{(current_progress[0] / port_range) * 100:.2f}%][{current_progress[0]}/{port_range}]", end='\r')


def multi_threaded_banner_grabbing(ip_lines, ports, threads, banner_sample):
    port_range = len(ports)
    current_progress = [0]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(banner_collector, port, ip.strip(),
                            banner_sample, port_range, current_progress)
            for ip in ip_lines for port in ports
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def banner_grabbing(threads, folder_sample):
    start_time = time.time()
    banner_sample = folder_sample + f'/active/banner_grabbing#'
    port_sample = folder_sample + f'/active/open_port.txt'

    unique_IPs_sample = folder_sample + '/active/unique_IPs.txt'
    with open(unique_IPs_sample, 'r') as file:
        IPs = file.read().splitlines()

    with open(port_sample, 'r') as file:
        open_port_lists = [port.strip() for port in file.readlines()]

    for ip in IPs:
        print(f'[-] Banner Grabbing On IP {ip}')
        multi_threaded_banner_grabbing(
            ip, open_port_lists, threads, banner_sample)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
