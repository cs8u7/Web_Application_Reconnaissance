import socket
import threading
from queue import Queue

# Target configuration
target = "127.0.0.1"  # Replace with your target IP or hostname
port_range = (1, 1024)  # Port range to scan

# Thread-safe queue to store ports
port_queue = Queue()
open_ports = []

# Function to scan a port
def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open")
                open_ports.append(port)
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Worker function for threading
def worker():
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(port)
        port_queue.task_done()

# Populate queue with ports
for port in range(port_range[0], port_range[1] + 1):
    port_queue.put(port)

# Start threading
threads = []
for _ in range(100):  # Number of threads
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Summary of open ports
print("Open ports:", open_ports)
