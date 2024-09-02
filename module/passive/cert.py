import requests
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import os
from termcolor import colored
from datetime import datetime

HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


def get_cert_ids(domain):
    url = "https://crt.sh/"
    params = {
        'output': "json",
        'Identity': domain
    }

    data = []
    response = requests.get(url, params=params, headers=HEADER).json()
    for cert in response:
        not_after = datetime.strptime(cert['not_after'], '%Y-%m-%dT%H:%M:%S')
        if not_after.year > 2023:
            data.append(cert['id'])

    return data


def get_cert(cert_id, cert_folder):
    cert_path = f'{cert_folder}/{cert_id}.pem'
    if not os.path.exists(cert_path):
        url = f"https://crt.sh/?d={cert_id}"
        response = requests.get(url, headers=HEADER)
        with open(cert_path, 'wb') as file:
            file.write(response.content)
    return cert_path


def get_subjectaltname(cert_path):
    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()
    subdomains = []
    try:
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        for ext in cert.extensions:
            if isinstance(ext.value, x509.SubjectAlternativeName):
                for name in ext.value.get_values_for_type(x509.DNSName):
                    if '*' not in name.lower():
                        subdomains.append(name.lower())
        return subdomains
    except Exception:
        return subdomains


def get_subdomains_with_cert(domain, cache, folder_sample):
    domain_sample = folder_sample + '/passive/subdomain_from_cert.txt'
    with open(domain_sample, 'w') as file:
        pass
    cert_folder = f'SSL_cert/{domain}'

    if cache and os.path.exists(cert_folder):
        print('[-] Decode Certificates From Storage')
        files = os.listdir(cert_folder)
        for file_name in files:
            if os.path.isfile(os.path.join(cert_folder, file_name)):
                with open(domain_sample, 'a') as file:
                    for subdomain in get_subjectaltname(f'{cert_folder}/{file_name}'):
                        file.write(f'{subdomain}\n')
    else:
        if cache:
            print(
                colored(f'[*] Cache of domain {domain} is missing', 'magenta'))
        print('[-] Download And Decode Certificates')
        crtsh_data = get_cert_ids(domain)
        for crtsh_id in crtsh_data:
            cert_path = get_cert(crtsh_id, cert_folder)
            with open(domain_sample, 'a') as file:
                for subdomain in get_subjectaltname(cert_path):
                    file.write(f'{subdomain}\n')

    with open(domain_sample, 'r') as file:
        lines = file.readlines()
    unique_lines = sorted(set(lines))
    with open(domain_sample, 'w') as file:
        file.writelines(unique_lines)
