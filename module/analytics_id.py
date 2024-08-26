import requests
import re

import pprint

def extract_ga_ids(domain):
   print('[-] Fetching Analytics UA ID')
   headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
   }

   url=f'https://{domain}'
   session = requests.Session()
   request = requests.Request('GET', url, headers=headers)
   prepared_request = session.prepare_request(request)

   response = session.send(prepared_request).text
    
   ua_pattern = r'UA-\d{4,9}'
   ua_ids = re.findall(ua_pattern, response)
   
   return ua_ids

def fetch_hacker_target(ua_id,domain_sample):
   domain_list = []
   try:
      url = f'https://api.hackertarget.com/analyticslookup/?q={ua_id}'
      response = requests.get(url)
      data = response.text
      
      if data == 'error getting results':
         return domain_list
      else:
         domain_list = data.splitlines()
         with open(domain_sample, 'a') as file:
            for item in domain_list:
               file.write(f"{item}\n")

      return domain_list
   except (requests.RequestException):
      return domain_list

def domain_by_analytic(domain,folder_sample):
   domain_sample = folder_sample + '/' + folder_sample + '@subdomain.txt'
   ua_id_list = extract_ga_ids(domain)
   print('[-] Fetching Hacker Target')
   for ua_id in ua_id_list:
      fetch_hacker_target(ua_id,domain_sample)

   with open(domain_sample, 'r') as file:
      lines = file.readlines()
   unique_lines = sorted(set(lines))
   with open(domain_sample, 'w') as file:
      file.writelines(unique_lines)
   
   
   
