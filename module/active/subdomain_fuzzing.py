import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

sub_count = 0

def fuzzing_subdomain_with_wordlist(subdomain, base_domain, subdomain_sample, sub_range):
    global sub_count
    sub_count += 1
    print(f"[{(sub_count / sub_range) * 100:.2f}%][{sub_count}/{sub_range}]", end='\r')
    target_url = f'http://{subdomain}.{base_domain}'
    try:
        response = requests.get(target_url, allow_redirects=False, timeout=30)
        if response.status_code == 200:
            with open(subdomain_sample, 'a') as file:
                file.write(f'[{response.status_code}] {target_url}\n')
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


def subdomain_fuzzing(base_domain, threads, output_folder):
    wordlist_file = 'module/active/word_list/subdomain.txt'
    subdomain_sample = f'{output_folder}/active/subdomain.txt'
    multi_threaded_subdomain_fuzzing(
        base_domain, threads, wordlist_file, subdomain_sample)
    
    print(f"", end='\r', flush=True)