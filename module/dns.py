import requests
import json
import dns.resolver

def fetch_networkcalc(domain):
   print('[-] Fetching networkcalc')
   IPs_v4 = []
   mail_servers = []

   try:
      url = f'https://networkcalc.com/api/dns/lookup/{domain}'
      response = requests.get(url)
      data = response.json()

      for record_A in data['records']['A']:
         IPs_v4.append(record_A['address'])

      for record_MX in data['records']['MX']:
         mail_servers.append(f"{record_MX['priority']} {record_MX['exchange']}")

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
      response = resolver.resolve(domain,record_type)
      for data in response:
         IPs.append(data)
      return IPs
   except Exception:
      return IPs

def dns_mail_server_query(domain, record_type, isp):
   resolver = dns.resolver.Resolver()
   resolver.nameservers = [isp]
   
   mail_servers = []
   try:
      response = resolver.resolve(domain,record_type)
      for data in response:
         mail_servers.append(f"{data.preference} {data.exchange}")
      return mail_servers
   except Exception:
      return mail_servers

def fetch_public_isp(domain,isp):
   return dns_ip_query(domain,'A',isp), dns_ip_query(domain,'AAAA',isp), dns_mail_server_query(domain,'MX',isp)

def ip_dns_lookup(domain,folder_sample):
   ip_dns_report = folder_sample + '/' + folder_sample + '@ip_dns.txt'
   networkcalc_ip_v4, networkcalc_mail_servers = fetch_networkcalc(domain)
   hackertarget_ip_v4, hackertarget_ip_v6, hackertarget_mail_servers = fetch_hackertarget(domain)
   gg_ip_v4, gg_ip_v6, gg_mail_servers = fetch_public_isp(domain,'8.8.8.8')
   cloudflare_ip_v4_1, cloudflare_ip_v6_1, cloudflare_mail_servers_1 = fetch_public_isp(domain,'1.1.1.1')
   cloudflare_ip_v4_2, cloudflare_ip_v6_2, cloudflare_mail_servers_2 = fetch_public_isp(domain,'1.0.0.1')
   
   ip_v4_set = networkcalc_ip_v4 + hackertarget_ip_v4 + gg_ip_v4 + cloudflare_ip_v4_1 + cloudflare_ip_v4_2
   ip_v6_set = hackertarget_ip_v6 + gg_ip_v6 + cloudflare_ip_v6_1 + cloudflare_ip_v6_2
   mail_servers_set = networkcalc_mail_servers + hackertarget_mail_servers + gg_mail_servers + cloudflare_mail_servers_1 + cloudflare_mail_servers_2
   
   with open(ip_dns_report, 'w') as file:
      file.write('IP V4 set:\n')
      for ip_v4 in list(set(ip_v4_set)):
         file.write(f'{ip_v4}\n')
      file.write('\n')

      file.write('IP V6 set:\n')
      for ip_v6 in list(set(ip_v6_set)):
         file.write(f'{ip_v6}\n')
      file.write('\n')

      file.write('Mail Server set:\n')
      for mx in list(set(mail_servers_set)):
         file.write(f'{mx}\n')
      file.write('\n')