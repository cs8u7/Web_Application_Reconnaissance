import socket
from concurrent.futures import ThreadPoolExecutor
import threading
import concurrent.futures

port_count = 0
port_lock = threading.Lock()
port_progress_lock = threading.Lock()


def scan_port(port, total_ports, domain, port_sample):
    global port_count
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            result = s.connect_ex((domain, port))
            if result == 0:
                with port_lock:
                    with open(port_sample, 'a') as file:
                        file.write(f'{port}\n')

        with port_progress_lock:
            port_count += 1
            print(
                f"[{(port_count / total_ports) * 100:.2f}%][{port_count}/{total_ports}]", end='\r')

    except Exception as e:
        pass


def multi_threaded_port_scan(threads, port_range, domain, port_sample):
    total_ports = port_range[1] - port_range[0] + 1
    ports = range(port_range[0], port_range[1] + 1)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(
            scan_port, port, total_ports, domain, port_sample) for port in ports]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def port_scanning(domain, threads, folder_result, port_start, port_end):
    port_sample = folder_result + f'/active/open_port.txt'
    port_range = (port_start, port_end)
    multi_threaded_port_scan(threads, port_range, domain, port_sample)

    with open(port_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(port_sample, 'w') as file:
        file.writelines(unique_lines)
