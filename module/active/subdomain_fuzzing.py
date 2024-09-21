import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading

REQUEST_TIMEOUT = 2
lock = threading.Lock()


def fuzzing_subdomain_with_wordlist(subdomain, base_domain, subdomain_sample, sub_range, current_count, results):
    target_url = f'https://{subdomain}.{base_domain}'

    try:
        response = requests.get(
            target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            results.append(f'{subdomain}.{base_domain}')

    except requests.RequestException:
        pass

    with lock:
        current_count[0] += 1
        print(
            f"[{(current_count[0] / sub_range) * 100:.2f}%][{current_count[0]}/{sub_range}]", end='\r')


def multi_threaded_subdomain_fuzzing(base_domain, threads, wordlist_file, subdomain_sample):
    with open(wordlist_file, 'r') as file:
        subdomains = file.read().splitlines()
    results = []

    sub_range = len(subdomains)
    current_count = [0]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(
                fuzzing_subdomain_with_wordlist, subdomain, base_domain, subdomain_sample, sub_range, current_count, results
            )
            for subdomain in subdomains
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass
    
    with open(subdomain_sample, 'a') as file:
        for subdomain in results:
            file.write(f'{subdomain}\n')
def subdomain_fuzzing(base_domain, threads, folder_result):
    start_time = time.time()
    wordlist_file = 'module/active/word_list/subdomain.txt'
    subdomain_sample = f'{folder_result}/active/subdomain.txt'

    multi_threaded_subdomain_fuzzing(
        base_domain, threads, wordlist_file, subdomain_sample)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
