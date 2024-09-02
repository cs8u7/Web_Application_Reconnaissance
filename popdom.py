import argparse
import sys
import re
from datetime import datetime
from termcolor import colored
import os
import shutil

from module.print_title import print_title
from module.passive.endpoint import fetch_urls
from module.passive.endpoint import hidden_and_document_endpoint
from module.passive.domain import subdomain_discover
from module.passive.dns import ip_dns_lookup
from module.passive.whois import whois_lookup
from module.passive.analytics_id import domain_by_analytic
from module.passive.cert import get_subdomains_with_cert

from module.active.ping import ping
from module.active.ping import active_ip_os_detection


def main():
    print_title()

    parser = argparse.ArgumentParser(
        description="Automate Reconnaissance Tool")
    parser.add_argument('-u', type=str, help="URL of target web application.")
    parser.add_argument('-p', action='store_true',
                        help="Specific passive recon")
    parser.add_argument('-a', action='store_true',
                        help="Specific active recon")
    parser.add_argument('-ipinfo', action='store_true',
                        help="Mark IPinfo key is trail or premium")
    parser.add_argument('-cert', action='store_true',
                        help="Enable domain discover with certificate")
    parser.add_argument('-cache', action='store_true',
                        help="Only use captured SSL certificate for domain discover")
    args = parser.parse_args()

    args_dict = vars(args)

    if not args.u:
        print(colored(
            "Error: The '-u' option is required. Please provide a valid URL.", "magenta"))
        sys.exit(1)

    if not (args.p or args.a):
        print("Error: You must provide either -p (passive recon) or -a (active recon).")
        sys.exit(1)

    encountered_options = []

    for option, value in args_dict.items():
        if value:
            if option in encountered_options:
                print(colored(
                    f"Error: Duplicate option detected: '{option}'. Please use each option only once.", "magenta"))
                sys.exit(1)
            else:
                encountered_options.append(option)

    url_pattern = re.compile(
        r'^((http|https):\/\/)?(?P<domain>[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})(:\d+)?(\/\S*)?$')
    match = url_pattern.match(args.u)

    if match:
        domain = match.group('domain')
        date = datetime.now().date()
        folder_result = str(date) + '#' + args.u
        
        if args.p:
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

            if args.cert:
                print(
                    colored('[+] Subdomain Discover With SSL Certificates', 'cyan'))
                if not os.path.exists(f'SSL_cert/{domain}'):
                    os.makedirs(f'SSL_cert/{domain}')
                get_subdomains_with_cert(domain, args.cache, folder_result)

            print(colored('[+] Hidden Endpoints & Document Filtering', 'cyan'))
            hidden_and_document_endpoint(endpoint_result, folder_result)

            print(colored('[+] IP Lookup and Reverse DNS Lookup', 'cyan'))
            ip_dns_lookup(domain, args.ipinfo, folder_result)

            print(colored('[+] WHOIS Lookup', 'cyan'))
            whois_lookup(domain, folder_result)

            print(
                colored('[+] Lookup New Domains by Google Analytics', 'cyan'))
            domain_by_analytic(domain, folder_result)

        elif args.a:
            if os.path.exists(f'{folder_result}/active') and os.path.isdir(f'{folder_result}/active'):
                shutil.rmtree(f'{folder_result}/active')
            os.makedirs(f'{folder_result}/active', exist_ok=True)
            print(colored(f'[**] Starting Active Recon', 'yellow'))
            print(colored('[+] Ping Sweeping', 'cyan'))
            ping(domain, folder_result)
            print(colored('[+] OS Detection', 'cyan'))
            active_ip_os_detection(folder_result)

    else:
        print(colored(
            "Error: The url has invalid form. Please provide a valid URL.", "magenta"))
        sys.exit(1)


if __name__ == '__main__':
    main()
    print(colored('[\/] DONE !!!', 'green'))
