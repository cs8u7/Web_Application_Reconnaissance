import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
from bs4 import BeautifulSoup


def get_html_snippet(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup)[:1000]


def parameter_fuzzing_unity(target_url, param, payload, param_sample, baseline_html):
    parsed_url = urllib.parse.urlparse(target_url)
    query = urllib.parse.parse_qs(parsed_url.query)
    query[param] = payload
    new_query = urllib.parse.urlencode(query, doseq=True)
    new_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
    try:
        response = requests.get(new_url, timeout=2)
        response_html = get_html_snippet(response)

        if response_html != baseline_html:
            with open(param_sample, 'a') as file:
                file.write(f'{target_url}/?{param}=\n')

    except requests.RequestException:
        pass


def multi_threaded_parameter_fuzzing(base_url, threads, param_sample, baseline_html):
    with open('module/active/word_list/param_input.txt', 'r') as file:
        payloads = file.read().splitlines()

    with open('module/active/word_list/param.txt', 'r') as file:
        params = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(parameter_fuzzing_unity, base_url, param, payload, param_sample, baseline_html): (param, payload)
            for param in params for payload in payloads
        }

        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass


def parameter_fuzzing(domain, threads, folder_result):
    param_sample = f'{folder_result}/active/parameter_results.txt'
    base_url = 'https://' + domain + "/"
    with open(param_sample, 'a') as file:
        pass
    with open(f'{folder_result}/active/web_content.txt', 'r') as file:
        baseline_html = file.read()[:1000]

    multi_threaded_parameter_fuzzing(
        base_url, threads, param_sample, baseline_html)
    
    with open(param_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(param_sample, 'w') as file:
        file.writelines(unique_lines)
