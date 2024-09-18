import requests
from concurrent.futures import ThreadPoolExecutor
import time

endpoint_count = 0
REQUEST_TIMEOUT = 5


def fuzz(target_url, endpoint_fuzzing_sample, endpoint_range):
    global endpoint_count
    endpoint_count += 1
    print(f"[{(endpoint_count / endpoint_range) * 100:.2f}%][{endpoint_count}/{endpoint_range}]", end='\r')

    try:
        response = requests.get(
            target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)

        with open(endpoint_fuzzing_sample, 'a') as file:
            file.write(f'[{response.status_code}] {target_url}\n')

    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass
    except requests.RequestException:
        pass


def multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample, domains_range):
    with open('module/active/word_list/endpoint.txt', 'r') as file:
        payloads = file.read().splitlines()

    endpoint_range = len(payloads) * domains_range

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(
                fuzz, target_url.format(
                    payload), endpoint_fuzzing_sample, endpoint_range
            )
            for payload in payloads
        ]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing future: {e}")


def endpoint_fuzzing(threads, folder_result):
    start_time = time.time()
    endpoint_fuzzing_sample = folder_result + f'/active/endpoint_fuzzing.txt'
    domain_sample = f'{folder_result}/active/subdomain.txt'
    with open(domain_sample, 'r') as file:
        domains = file.read().splitlines()
    domains_range = len(domains)

    for domain in domains:
        target_url = 'https://' + domain + "/{}"
        print(f'[-] Fuzzing Domain {domain}')
        multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample, domains_range)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
