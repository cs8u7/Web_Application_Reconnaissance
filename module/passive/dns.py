import requests
import json
import dns.resolver
from dotenv import load_dotenv
from termcolor import colored
import os
import ipinfo
import socket
import asyncio

import pprint


def fetch_networkcalc(domain):
    print('[-] Fetching networkcalc')
    IPs_v4 = []
    mail_servers = []

    try:
        url = f'https://networkcalc.com/api/dns/lookup/{domain}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'NO_RECORDS':
            return IPs_v4, mail_servers
        else:
            for record_A in data['records']['A']:
                IPs_v4.append(record_A['address'])

            for record_MX in data['records']['MX']:
                mail_servers.append(
                    f"{record_MX['priority']} {record_MX['exchange']}")

        return IPs_v4, mail_servers
    except (requests.RequestException, json.JSONDecodeError):
        return IPs_v4, mail_servers


def fetch_hackertarget(domain):
    print('[-] Fetching Hacker Target')
    IPs_v4 = []
    IPs_v6 = []
    mail_servers = []

    try:
        url = f'https://api.hackertarget.com/dnslookup/?q={domain}&output=json'
        response = requests.get(url)
        data = response.json()

        if 'error' in data:
            return IPs_v4, IPs_v6, mail_servers
        else:
            for record_A in data['A']:
                IPs_v4.append(record_A)

            for record_AAAA in data['AAAA']:
                IPs_v6.append(record_AAAA)

            for record_MX in data['MX']:
                mail_servers.append(record_MX)

        return IPs_v4, IPs_v6, mail_servers
    except (requests.RequestException, json.JSONDecodeError):
        return IPs_v4, IPs_v6, mail_servers


def dns_ip_query(domain, record_type, isp):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [isp]

    IPs = []
    try:
        response = resolver.resolve(domain, record_type)
        for data in response:
            IPs.append(str(data))
        return IPs
    except Exception:
        return IPs


def dns_mail_server_query(domain, record_type, isp):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [isp]

    mail_servers = []
    try:
        response = resolver.resolve(domain, record_type)
        for data in response:
            mail_servers.append(f"{data.preference} {data.exchange}")
        return mail_servers
    except Exception:
        return mail_servers


def fetch_public_isp(domain, isp):
    return dns_ip_query(domain, 'A', isp), dns_ip_query(domain, 'AAAA', isp), dns_mail_server_query(domain, 'MX', isp)


def fetch_ipinfo_localtion(ip, is_trial, api_key):

    handler = ipinfo.getHandler(api_key)

    async def do_req():
        details = handler.getDetails(ip)
        if is_trial:
            return f'{details.all["ip"]} Contact: {details.all["abuse"]["email"]}#{details.all["abuse"]["name"]}#{details.all["abuse"]["phone"]} Org: {details.all["company"]["name"]}# Region:{details.all["company"]["domain"]} {details.all["region"]}'
        else:
            return f'{details.all["ip"]} Org: {details.all["org"]} Region: {details.all["region"]} Postal: {details.all["postal"]}'

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(do_req())
    return result


def fetching_reverse_dns_ipinfo(ip, api_key):
    try:
        url = f'https://ipinfo.io/domains/{ip}?token={api_key}'
        response = requests.get(url)
        data = response.json()

        return data['domains']

    except (requests.RequestException, json.JSONDecodeError):
        return []


def fetch_viewdns_reverse_ip(ip, api_key):
    dns = []

    url = f'https://api.viewdns.info/reverseip/?host={ip}&apikey={api_key}&output=json'
    response = requests.get(url)
    data = response.json()

    return dns


def fetch_viewdns_ip_history(domain, api_key):
    history_IPs = []

    try:
        url = f'https://api.viewdns.info/iphistory/?domain={domain}&apikey={api_key}&output=json'
        response = requests.get(url, timeout=120)
        data = response.json()

        for record in data['response']['records']:
            history_IPs.append(record['ip'])
        return history_IPs

    except (requests.RequestException, json.JSONDecodeError):
        return history_IPs


def ip_dns_lookup(domain, is_trial, folder_sample):
    networkcalc_ip_v4, networkcalc_mail_servers = fetch_networkcalc(domain)
    hackertarget_ip_v4, hackertarget_ip_v6, hackertarget_mail_servers = fetch_hackertarget(
        domain)
    print('[-] Fetching Google ISP')
    gg_ip_v4, gg_ip_v6, gg_mail_servers = fetch_public_isp(domain, '8.8.8.8')
    print('[-] Fetching Cloudflare ISP')
    cloudflare_ip_v4_1, cloudflare_ip_v6_1, cloudflare_mail_servers_1 = fetch_public_isp(
        domain, '1.1.1.1')
    cloudflare_ip_v4_2, cloudflare_ip_v6_2, cloudflare_mail_servers_2 = fetch_public_isp(
        domain, '1.0.0.1')

    ip_v4_set = list(set(networkcalc_ip_v4 + hackertarget_ip_v4 +
                     gg_ip_v4 + cloudflare_ip_v4_1 + cloudflare_ip_v4_2))
    ip_v6_set = list(set(hackertarget_ip_v6 + gg_ip_v6 +
                     cloudflare_ip_v6_1 + cloudflare_ip_v6_2))
    mail_servers_set = list(set(networkcalc_mail_servers + hackertarget_mail_servers +
                            gg_mail_servers + cloudflare_mail_servers_1 + cloudflare_mail_servers_2))

    ipv4_sample = folder_sample + '/passive/ipv4.txt'
    with open(ipv4_sample, 'w') as file:
        for ip_v4 in ip_v4_set:
            file.write(f'{ip_v4}\n')

    ipv6_sample = folder_sample + '/passive/ipv6.txt'
    with open(ipv6_sample, 'w') as file:
        for ip_v6 in ip_v6_set:
            file.write(f'{ip_v6}\n')

    mail_servers_sample = folder_sample + '/passive/mail_servers.txt'
    with open(mail_servers_sample, 'w') as file:
        for mx in mail_servers_set:
            file.write(f'{mx}\n')

    load_dotenv()
    print(colored('[+] IP History', 'cyan'))
    print('[-] Fetching ViewDNS')
    api_key_viewdns = os.getenv('VIEWDNS_API_KEY')
    ip_history_sample = folder_sample + '/passive/ip_history.txt'
    if api_key_viewdns:
        history_IPs = fetch_viewdns_ip_history(domain, api_key_viewdns)
        with open(ip_history_sample, 'w') as file:
            for ip in history_IPs:
                file.write(f'{ip}\n')

    api_key_ipinfo = os.getenv('IPinfo_API_KEY')
    print(colored('[+] Localtion, Hosting Provider, Region', 'cyan'))
    if api_key_ipinfo:
        print('[-] Fetching IPinfo')
        location_sample = folder_sample + '/passive/ip_history.txt'
        with open(location_sample, 'w') as file:
            for ip in ip_v4_set:
                text = fetch_ipinfo_localtion(ip, is_trial, api_key_ipinfo)
                file.write(f'{text}\n')

    print(colored('[+] Reverse IP Lookup', 'cyan'))
    reverse_dns_set = []

    if api_key_viewdns:
        print('[-] Fetching ViewDNS')
        reverse_dns_sample = folder_sample + '/passive/ip_history.txt'
        for ip in ip_v4_set:
            reverse_dns_set = reverse_dns_set + \
                fetch_viewdns_reverse_ip(ip, api_key_viewdns)
    filter_reverse_dns_set = list(set(reverse_dns_set))
    with open(reverse_dns_sample, 'w') as file:
        for reverse_dns in filter_reverse_dns_set:
            file.write(f'{reverse_dns}\n')
