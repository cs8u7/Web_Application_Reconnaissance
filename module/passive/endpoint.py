import requests
import json
import os
from dotenv import load_dotenv
import time 
from datetime import datetime
import re

def fetch_wayback_urls(domain, sample):
    print('[-] Fetching WayBack')
    current_year = datetime.now().year
    start_year = current_year - 3

    url = (f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey&from={start_year}&to={current_year}")
    try:
        response = requests.get(url, timeout=600)
        response.raise_for_status()
        data = response.json()

        result = [item[2] for item in data[1:]]

        with open(sample, 'a') as file:
            file.write("\n\n")
            for item in result:
                file.write(f"{item}\n")
    except (requests.RequestException, json.JSONDecodeError):
        pass


def fetch_commoncrawl_urls(domain, sample):
    print('[-] Fetching Common Crawl')
    urls = []
    url = f"http://index.commoncrawl.org/CC-MAIN-2018-22-index?url=*.{domain}/*&output=json"

    try:
        response = requests.get(url, timeout=600)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                item = json.loads(line)
                urls.append(item.get('url'))

        with open(sample, 'a') as file:
            file.write("\n\n")
            for item in urls:
                file.write(f"{item}\n")
    except (requests.RequestException, json.JSONDecodeError):
        pass


def fetch_virustotal_urls(domain, sample):
    print('[-] Fetching Virus total')
    urls = []
    api_key = os.getenv('VT_API_KEY')
    if not api_key:
        return urls

    try:
        load_dotenv()
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'apikey': os.getenv('VT_API_KEY'), 'domain': domain}
        response = requests.get(url, params=params)
        data = response.json()

        if data['verbose_msg'] == 'Domain not found':
            return

        undetected_urls = []
        detected_urls = []
        if data['detected_urls'].__len__() != 0:
            for url in data['detected_urls']:
                detected_urls.append(url['url'])
        elif data['undetected_urls'].__len__() != 0:
            for url in data['undetected_urls']:
                undetected_urls.append(url[0])

        combined_urls = undetected_urls + detected_urls
        urls = list(set(combined_urls))

        with open(sample, 'a') as file:
            file.write("\n\n")
            for item in urls:
                file.write(f"{item}\n")
    except (requests.RequestException, json.JSONDecodeError):
        pass


def fetch_urls(domain, sample):
    start_time = time.time()
    fetch_commoncrawl_urls(domain, sample)
    fetch_virustotal_urls(domain, sample)
    fetch_wayback_urls(domain, sample)

    with open(sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    
    cleaned_lines = [line for line in unique_lines if '.css' not in line]
    
    with open(sample, 'w') as file:
        file.writelines(cleaned_lines)
    
    end_time = time.time()
    running = end_time - start_time 
    print(f"[Time]: {running:.2f}s")


def hidden_and_document_endpoint(endpoint_sample, folder_sample):
    start_time = time.time()
    hidden_sample = folder_sample + '/passive/hidden.txt'
    print('[-] Reading URLs')
    with open(endpoint_sample, 'r') as file:
        url_lines = file.readlines()
    with open('module/passive/hidden_wordlist.txt', 'r') as file:
        hidden_lines = file.readlines()

    print('[-] Hidden Endpoint Filtering')
    hidden_set = []
    for url_line in url_lines:
        for hidden_word in hidden_lines:
            if hidden_word in url_line:
                hidden_set.append(url_line)
                break

    with open(hidden_sample, 'w') as file:
        pass
    with open(hidden_sample, 'w') as file:
        file.writelines(hidden_set)

    document_sample = folder_sample + '/passive/document.txt'
    document_set = []
    doc_temps = ['.txt', '.pdf', '.doc', '.xlsx',
                 '.xls', '.ods', '.docx', '.ppt', '.pptx','.json']
    print('[-] Document Filtering')
    hidden_set = []
    for url_line in url_lines:
        for doc in doc_temps:
            if doc in url_line:
                document_set.append(url_line)
                break

    with open(document_sample, 'w') as file:
        pass
    with open(document_sample, 'w') as file:
        file.writelines(document_set)

    end_time = time.time()
    running = end_time - start_time 
    print(f"[Time]: {running:.2f}s")
