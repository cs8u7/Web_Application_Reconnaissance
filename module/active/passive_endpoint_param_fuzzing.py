import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time

endpoint_count = 0
REQUEST_TIMEOUT = 2


def check_domain_in_url(target_url, domains):
    parsed_url = urlparse(target_url)
    target_domain = parsed_url.netloc

    for domain in domains:
        if domain in target_domain:
            return True

    return False


def check_params_in_url(target_url):
    parsed_url = urlparse(target_url)
    return bool(parsed_url.query)


def fuzz(target_url, domains, endpoint_range, endpoint_results, param_result):
    global endpoint_count
    endpoint_count += 1
    print(f"[{(endpoint_count / endpoint_range) * 100:.2f}%][{endpoint_count}/{endpoint_range}]", end='\r')

    if check_domain_in_url(target_url, domains):
        try:
            response = requests.get(
                target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                endpoint_results.append(target_url)
                if check_params_in_url(target_url):
                    param_result.append(target_url)

        except requests.Timeout:
            pass
        except requests.ConnectionError:
            pass
        except requests.RequestException:
            pass


def multi_threads_fuzzing(threads, endpoint_fuzzing_sample, endpoint_result_sample, domains, param_sample):
    with open(endpoint_fuzzing_sample, 'r') as file:
        targets = file.read().splitlines()
    endpoint_results = []
    param_result = []

    endpoint_range = len(targets)
    
    if endpoint_range < threads:
        max_threads = endpoint_range

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(
                fuzz, target, domains, endpoint_range, endpoint_results, param_result
            )
            for target in targets
        ]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing future: {e}")

    with open(endpoint_result_sample, 'a') as file:
        for endpoint in endpoint_results:
            file.write(f'{endpoint}\n')

    with open(param_sample, 'a') as file:
        for param_payload in param_result:
            file.write(f'{param_payload}\n')


def passive_endpoint_param_fuzzing(threads, folder_result):
    start_time = time.time()
    endpoint_result_sample = folder_result + f'/active/endpoint_fuzzing.txt'
    endpoint_fuzzing_sample = folder_result + f'/passive/endpoint.txt'

    domain_sample = folder_result + f'/active/subdomain.txt'
    with open(domain_sample, 'r') as file:
        domains = file.read().splitlines()

    param_sample = f'{folder_result}/active/parameter_results.txt'

    multi_threads_fuzzing(threads, endpoint_fuzzing_sample,
                          endpoint_result_sample, domains, param_sample)

    with open(endpoint_result_sample, 'r') as file:
        endpoint_lines = file.readlines()
    unique_endpoints = sorted(set(endpoint_lines))
    with open(endpoint_result_sample, 'w') as file:
        file.writelines(unique_endpoints)

    with open(param_sample, 'r') as file:
        param_lines = file.readlines()
    unique_params = sorted(set(param_lines))
    with open(param_sample, 'w') as file:
        file.writelines(unique_params)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
