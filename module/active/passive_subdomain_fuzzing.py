import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

sub_count = 0
REQUEST_TIMEOUT = 2


def fuzzing_subdomain_with_wordlist(subdomain, sub_range, results):
    global sub_count
    sub_count += 1
    print(f"[{(sub_count / sub_range) * 100:.2f}%][{sub_count}/{sub_range}]", end='\r')
    target_url = f'https://{subdomain}'
    try:
        response = requests.get(
            target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            results.append(subdomain)

    except requests.RequestException:
        pass


def multi_threaded_subdomain_fuzzing(threads, wordlist_file, subdomain_sample):
    with open(wordlist_file, 'r') as file:
        subdomains = file.read().splitlines()
    results = []

    sub_range = len(subdomains)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(fuzzing_subdomain_with_wordlist, subdomain,
                                   sub_range, results): subdomain for subdomain in subdomains}

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass

    with open(subdomain_sample, 'a') as file:
        for subdomain in results:
            file.write(f'{subdomain}\n')


def passive_subdomain_fuzzing(threads, folder_result):
    start_time = time.time()
    wordlist_file = f'{folder_result}/passive/subdomain.txt'
    subdomain_sample = f'{folder_result}/active/subdomain.txt'
    multi_threaded_subdomain_fuzzing(
        threads, wordlist_file, subdomain_sample)

    with open(subdomain_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(subdomain_sample, 'w') as file:
        file.writelines(unique_lines)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
