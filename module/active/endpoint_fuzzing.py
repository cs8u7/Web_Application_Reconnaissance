import requests
from concurrent.futures import ThreadPoolExecutor
import time
import threading

REQUEST_TIMEOUT = 2
lock = threading.Lock()


def fuzz(target_url, endpoint_range, current_line, results):
    with lock:
        current_line[0] += 1
        print(f"[{(current_line[0] / endpoint_range) * 100:.2f}%][{current_line[0]}/{endpoint_range}]", end='\r')

    try:
        response = requests.get(
            target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            results.append(target_url)

    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass
    except requests.RequestException:
        pass


def multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample):
    with open('module/active/word_list/endpoint.txt', 'r') as file:
        payloads = file.read().splitlines()
    results = []

    endpoint_range = len(payloads)
    current_line = [0]
    if endpoint_range < threads:
        max_threads = endpoint_range
    else:
        max_threads= threads

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(
                fuzz, target_url.format(
                    payload), endpoint_range, current_line, results
            )
            for payload in payloads
        ]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                pass

    with open(endpoint_fuzzing_sample, 'a') as file:
        for endpoint in results:
            file.write(f'{endpoint}\n')


def endpoint_fuzzing(threads, folder_result):
    start_time = time.time()
    endpoint_fuzzing_sample = folder_result + f'/active/endpoint_fuzzing.txt'
    domain_sample = f'{folder_result}/active/subdomain.txt'

    with open(domain_sample, 'r') as file:
        domains = file.read().splitlines()

    for domain in domains:
        target_url = 'https://' + domain + "/{}"
        print(f'[-] Endpoint Fuzzing On Domain {domain}')
        multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
