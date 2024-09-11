import requests
from concurrent.futures import ThreadPoolExecutor

endpoint_count = 0
REQUEST_TIMEOUT = 10

def fuzz(target_url, endpoint_fuzzing_sample, endpoint_range):
    global endpoint_count
    endpoint_count += 1
    print(f"[{(endpoint_count / endpoint_range) * 100:.2f}%][{endpoint_count}/{endpoint_range}]", end='\r')
    
    try:
        response = requests.get(target_url, allow_redirects=False, timeout=REQUEST_TIMEOUT)

        with open(endpoint_fuzzing_sample, 'a') as file:
            file.write(f'[{response.status_code}] {target_url}\n')
    
    except requests.Timeout:
        with open(endpoint_fuzzing_sample, 'a') as file:
            file.write(f"[Time out] {target_url}\n")
    except requests.ConnectionError:
        with open(endpoint_fuzzing_sample, 'a') as file:
            file.write(f"[Error connect] {target_url}\n")
    except requests.RequestException:
        with open(endpoint_fuzzing_sample, 'a') as file:
            file.write(f"[Error request] {target_url}\n")

def multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample):
    with open('module/active/word_list/endpoint.txt', 'r') as file:
        payloads = file.read().splitlines()
    
    endpoint_range = len(payloads)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(
                fuzz, target_url.format(payload), endpoint_fuzzing_sample, endpoint_range
            ) 
            for payload in payloads
        ]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing future: {e}")

def endpoint_fuzzing(domain, threads, folder_result):
    endpoint_fuzzing_sample = folder_result + f'/active/endpoint_fuzzing.txt'
    target_url = 'https://' + domain + "/{}"
    multi_threads_fuzzing(target_url, threads, endpoint_fuzzing_sample)

    print(f"", end='\r', flush=True)
