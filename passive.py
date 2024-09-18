import os
import shutil
from termcolor import colored

from module.passive.endpoint import fetch_urls
from module.passive.endpoint import hidden_and_document_endpoint
from module.passive.domain import subdomain_discover
from module.passive.dns import ip_dns_lookup
from module.passive.whois import whois_lookup
from module.passive.analytics_id import domain_by_analytic
from module.passive.cert import get_subdomains_with_cert
from module.passive.domain_summary import domain_summary


def passive_recon(domain, folder_result, cert, cache, ipinfo):
    if os.path.exists(f'{folder_result}/passive') and os.path.isdir(f'{folder_result}/passive'):
        shutil.rmtree(f'{folder_result}/passive')
    os.makedirs(f'{folder_result}/passive', exist_ok=True)
    print(
        colored(f'[+] Create Sample Folder {folder_result}', 'yellow'))
    print(colored(f'[**] Starting Passive Recon', 'yellow'))

    print(colored('[+] Endpoint Discover', 'cyan'))
    endpoint_result = folder_result + '/passive/endpoint.txt'
    with open(endpoint_result, 'w') as file:
        pass
    fetch_urls(domain, endpoint_result)

    print(colored('[+] Subdomain Discover', 'cyan'))
    subdomain_discover(domain, endpoint_result, folder_result)

    if cert:
        print(
            colored('[+] Subdomain Discover With SSL Certificates', 'cyan'))
        if not os.path.exists(f'SSL_cert/{domain}'):
            os.makedirs(f'SSL_cert/{domain}')
        get_subdomains_with_cert(domain, cache, folder_result)

    print(colored('[+] Hidden Endpoints & Document Filtering', 'cyan'))
    hidden_and_document_endpoint(endpoint_result, folder_result)

    print(colored('[+] IP Lookup and Reverse DNS Lookup', 'cyan'))
    ip_dns_lookup(domain, ipinfo, folder_result)

    print(colored('[+] WHOIS Lookup', 'cyan'))
    whois_lookup(domain, folder_result)

    print(
        colored('[+] Lookup New Domains by Google Analytics', 'cyan'))
    domain_by_analytic(domain, folder_result)

    print(
        colored('[+] Sumary Subdomains', 'cyan'))
    domain_summary(domain, folder_result)
