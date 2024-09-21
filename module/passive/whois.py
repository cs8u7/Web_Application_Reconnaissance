import requests
import json
from dotenv import load_dotenv
import os
import whois
import whois.whois
import subprocess
import time

def fetch_whois_libary(domain, whois_sample):
    print('[-] Direct query with WHOIS libary')

    try:
        domain_in4 = whois.whois(domain)
        if domain_in4['domain_name'] != None:
            with open(whois_sample, 'w') as file:
                file.write(f"domain name: {domain_in4['domain_name']}\n")
                file.write(f"registrar: {domain_in4['registrar']}\n")
                file.write(f"whois_server: {domain_in4['whois_server']}\n")
                file.write(f"emails: {domain_in4['emails']}\n")
                file.write(f"name: {domain_in4['name']}\n")
                file.write(f"org: {domain_in4['org']}\n")
                file.write(f"address: {domain_in4['address']}\n")
                file.write(f"city: {domain_in4['city']}\n")
                file.write(f"country: {domain_in4['country']}\n")
                file.write(
                    f"registrant_postal_code: {domain_in4['registrant_postal_code']}\n")
            return True
        else:
            return None
    except Exception:
        return None


def fetch_rapid_api(domain, whois_sample, api_key):
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
        if 'messages' in response:
            pass
        else:
            with open(whois_sample, 'w') as file:
                file.write(f'{response["rawdata"][0]}\n')
    except (requests.RequestException, json.JSONDecodeError):
        pass


def fetch_whois_command(domain, whois_sample):
    print('[-] Direct query with WHOIS comamnd')
    try:
        result = subprocess.run(
            ["whois", domain], capture_output=True, text=True)
        if 'no whois server' in result.stdout:
            return None
        else:
            with open(whois_sample, 'w') as file:
                file.write(result.stdout)
            return True
    except Exception as e:
        return None


def whois_lookup(domain, folder_sample):
    start_time = time.time()
    whois_sample = folder_sample + '/passive/WHOIS.txt'

    load_dotenv()
    api_key = os.getenv('RAPID_WHOIS_API_KEY')

    result_state_1 = fetch_rapid_api(domain, whois_sample, api_key)
    if not result_state_1:
        result_state_2 = fetch_whois_libary(domain, whois_sample)
        if not result_state_2:
            if api_key:
                fetch_whois_command(domain, whois_sample)
    
    end_time = time.time()
    running = end_time - start_time 
    print(f"[Time]: {running:.2f}s")
