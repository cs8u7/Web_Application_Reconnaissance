import requests
import json
import os
from dotenv import load_dotenv
import re


def fetch_virustotal(domain, sample):
    print('[-] Fetching Virus total')
    load_dotenv()
    api_key = os.getenv('VT_API_KEY')
    if not api_key:
        return

    try:
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'apikey': os.getenv('VT_API_KEY'), 'domain': domain}
        response = requests.get(url, params=params)
        data = response.json()

        if data['verbose_msg'] == 'Domain not found':
            return

        domain_list = data['subdomains']
        with open(sample, 'a') as file:
            for item in domain_list:
                file.write(f"{item}\n")
    except (requests.RequestException, json.JSONDecodeError):
        pass


def extract_endpoint_sample(endpoint_sample, domain_sample):
    subdomain_set = []
    print('[-] Extract Endpoint Sample')
    with open(endpoint_sample, 'r') as file:
        filedata = file.readlines()
    line_number = len(filedata)
    count = 0
    for line in filedata:
        count += 1
        print(
            f"[{(count/line_number)*100:.2f}%] [{count}/{line_number}]", end='\r')
        linedata = line.split('/')
        if linedata.__len__() > 2:
            if subdomain_set.__len__() == 0:
                subdomain_set.append(linedata[2])
            elif linedata[2] not in subdomain_set:
                subdomain_set.append(linedata[2])

    with open(domain_sample, 'a') as file:
        for item in subdomain_set:
            file.write(f"{item}\n")


def subdomain_discover(domain, endpoint_sample, folder_sample):
    domain_sample = folder_sample + '/passive/subdomain.txt'
    with open(domain_sample, 'w') as file:
        pass
    fetch_virustotal(domain, domain_sample)
    extract_endpoint_sample(endpoint_sample, domain_sample)

    with open(domain_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(domain_sample, 'w') as file:
        file.writelines(unique_lines)
