import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

sub_count = 0
REQUEST_TIMEOUT = 5

def fuzzing_subdomain_with_wordlist(subdomain, base_domain, subdomain_sample, sub_range):
    global sub_count
    sub_count += 1
    print(f"[{(sub_count / sub_range) * 100:.2f}%][{sub_count}/{sub_range}]", end='\r')
    target_url = f'https://{subdomain}.{base_domain}'
    try:
        response = requests.get(target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            with open(subdomain_sample, 'a') as file:
                file.write(f'{subdomain}.{base_domain}\n')
    except requests.RequestException:
        pass


def multi_threaded_subdomain_fuzzing(base_domain, threads, wordlist_file, subdomain_sample):
    with open(wordlist_file, 'r') as file:
        subdomains = file.read().splitlines()

    sub_range = len(subdomains)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(fuzzing_subdomain_with_wordlist, subdomain,
                                   base_domain, subdomain_sample, sub_range): subdomain for subdomain in subdomains}

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def subdomain_fuzzing(base_domain, threads, folder_result):
    start_time = time.time()
    wordlist_file = 'module/active/word_list/subdomain.txt'
    subdomain_sample = f'{folder_result}/active/subdomain.txt'
    multi_threaded_subdomain_fuzzing(
        base_domain, threads, wordlist_file, subdomain_sample)
    
    end_time = time.time()
    running = end_time - start_time 
    print(f"\n[Time]: {running:.2f}s")