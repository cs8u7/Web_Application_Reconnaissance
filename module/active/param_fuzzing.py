import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from bs4 import BeautifulSoup
import threading

REQUEST_TIMEOUT = 2
lock = threading.Lock()


def get_html_snippet(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup)[:1000]


def parameter_fuzzing_unity(url, param, param_sample, baseline_html, current_line, total_lines):
    try:
        payload = f'{url}/?{param}=1'
        response = requests.get(payload, timeout=REQUEST_TIMEOUT)
        response_html = get_html_snippet(response)

        if response_html != baseline_html:
            with open(param_sample, 'a') as file:
                file.write(f'{url}/?{param}=1\n')

    except requests.RequestException:
        pass

    # Update and print percentage progress for the wordlist
    with lock:
        current_line[0] += 1
        percent_params = (current_line[0] / total_lines) * 100
        print(f"[{percent_params:.2f}%]"
              f"[{current_line[0]}/{total_lines}]", end='\r', flush=True)


def multi_threaded_parameter_fuzzing(url, threads, param_sample, baseline_html, params):
    total_lines = len(params)
    current_line = [0]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(parameter_fuzzing_unity, url, param,
                            param_sample, baseline_html, current_line, total_lines)
            for param in params
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def parameter_fuzzing(threads, folder_result):
    start_time = time.time()
    param_sample = f'{folder_result}/active/parameter_results.txt'
    domain_sample = f'{folder_result}/active/subdomain.txt'

    with open(domain_sample, 'r') as file:
        domains = file.read().splitlines()

    for domain in domains:
        print(f'[-] Parameter Fuzzing On Domain {domain}')
        url = 'https://' + domain
        with open(param_sample, 'a') as file:
            pass

        web_content_sample = folder_result + \
            f'/active/web_content/{domain}.txt'
        with open(web_content_sample, 'r') as file:
            baseline_html = file.read()[:1000]

        with open('module/active/word_list/param.txt', 'r') as file:
            params = file.read().splitlines()

        multi_threaded_parameter_fuzzing(
            url, threads, param_sample, baseline_html, params)

        with open(param_sample, 'r') as file:
            lines = file.readlines()
        unique_lines = sorted(set(lines))
        with open(param_sample, 'w') as file:
            file.writelines(unique_lines)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Total Time]: {running:.2f}s")
