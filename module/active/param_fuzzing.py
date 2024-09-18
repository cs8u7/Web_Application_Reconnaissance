import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from bs4 import BeautifulSoup
import threading

current_line = 0
lock = threading.Lock()
REQUEST_TIMEOUT = 5

def get_html_snippet(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup)[:1000]

def parameter_fuzzing_unity(url, param, param_sample, baseline_html, total_lines):
    global current_line
    try:
        payload = f'{url}/?{param}=1'
        response = requests.get(payload, timeout=REQUEST_TIMEOUT)
        response_html = get_html_snippet(response)

        if response_html != baseline_html:
            with open(param_sample, 'a') as file:
                file.write(f'{url}/?{param}=1\n')

    except requests.RequestException:
        pass

    with lock:
        current_line += 1
        print(f"[{(current_line / total_lines) * 100:.2f}%][{current_line}/{total_lines}]", end='\r', flush=True)

def multi_threaded_parameter_fuzzing(url, threads, param_sample, baseline_html, params, total_lines):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(parameter_fuzzing_unity, url, param, param_sample, baseline_html, total_lines)
            for param in params
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass

def parameter_fuzzing(domain, threads, folder_result):
    start_time = time.time()
    param_sample = f'{folder_result}/active/parameter_results.txt'
    url = 'https://' + domain
    with open(param_sample, 'a') as file:
        pass
    
    with open(f'{folder_result}/active/web_content.txt', 'r') as file:
        baseline_html = file.read()[:1000]

    with open('module/active/word_list/param.txt', 'r') as file:
        params = file.read().splitlines()

    total_lines = len(params)

    multi_threaded_parameter_fuzzing(
        url, threads, param_sample, baseline_html, params, total_lines)

    with open(param_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(param_sample, 'w') as file:
        file.writelines(unique_lines)
    
    end_time = time.time()
    running = end_time - start_time 
    print(f"\n[Time]: {running:.2f}s")
