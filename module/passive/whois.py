import requests
import json
from dotenv import load_dotenv
import os

import pprint


def fetch_networkcalc(domain, whois_sample):
    print('[-] Fetching networkcalc')

    try:
        data = requests.get(
            f"https://networkcalc.com/api/dns/whois/{domain}").json()

        with open(whois_sample, 'w') as file:
            file.write(f"{data['whois']['abuse_email']}\n")
            file.write(f"{data['whois']['abuse_phone']}\n")
            file.write(f"{data['whois']['registrar']}\n")
            file.write(f"{data['whois']['registry_domain_id']}\n")

    except (requests.RequestException, json.JSONDecodeError):
        return


def fetch_whoisxml(domain, whois_sample, api_key):
    print('[-] Fetching Rapid API')

    try:
        url = "https://zozor54-whois-lookup-v1.p.rapidapi.com/"
        querystring = {"domain": domain,
                       "format": "json", "_forceRefresh": "0"}

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "zozor54-whois-lookup-v1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers,
                                params=querystring).json()

        with open(whois_sample, 'w') as file:
            file.write(f'{response["rawdata"][0]}\n')

    except (requests.RequestException, json.JSONDecodeError):
        return


def whois_lookup(domain, folder_sample):
    whois_sample = folder_sample + '/passive/WHOIS.txt'

    load_dotenv()
    api_key = os.getenv('RAPID_WHOIS_API_KEY')

    if not api_key:
        fetch_networkcalc(domain, whois_sample)
    else:
        fetch_whoisxml(domain, whois_sample, api_key)
