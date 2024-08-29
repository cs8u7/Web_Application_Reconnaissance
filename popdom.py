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

def main():
   parser = argparse.ArgumentParser(description="Automate Reconnaissance Tool")
   parser.add_argument('-u', type=str, help="URL of target web application.")
   parser.add_argument('-ipinfo', action='store_true', help="Mark IPinfo key is trail or premium")
   parser.add_argument('-cert', action='store_true', help="Enable domain discover with certificate")
   parser.add_argument('-cache', action='store_true', help="Only use captured SSL certificate for domain discover")
   args = parser.parse_args()

   if len(sys.argv) == 1:
      parser.print_help()
      sys.exit(1)

   url_pattern = re.compile(r'^((http|https):\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/\S*)?$')
   print_title()

   if args.u:                                                                
      if url_pattern.match(args.u):

         date = datetime.now().date()
         folder_result = str(date) + '#' + args.u
         if os.path.exists(folder_result) and os.path.isdir(folder_result):
            shutil.rmtree(folder_result)
         os.makedirs(folder_result, exist_ok=True)
         print(colored(f'[+] Create Sample Folder {folder_result}','yellow'))
         
         print(colored('[+] Endpoint Discover','cyan'))
         endpoint_result = folder_result + '/' +folder_result + '@endpoint.txt'
         with open(endpoint_result, 'w') as file:
            pass 
         fetch_urls(args.u,endpoint_result)

         print(colored('[+] Subdomain Discover','cyan'))
         subdomain_discover(args.u,endpoint_result,folder_result)

         if args.cert:
            print(colored('[+] Subdomain Discover With SSL Certificates','cyan'))
            if not os.path.exists(f'SSL_cert/{args.u}'):
               os.makedirs(f'SSL_cert/{args.u}')
            get_subdomains_with_cert(args.u,args.cache,folder_result)

         print(colored('[+] Hidden Endpoints & Document Filtering','cyan'))
         hidden_and_document_endpoint(endpoint_result,folder_result)

         print(colored('[+] IP Lookup and Reverse DNS Lookup','cyan'))
         ip_dns_lookup(args.u,args.ipinfo,folder_result)

         print(colored('[+] WHOIS Lookup','cyan'))
         whois_lookup(args.u,folder_result)

         print(colored('[+] Lookup New Domains by Google Analytics','cyan'))
         domain_by_analytic(args.u,folder_result)

         print(colored('[\/] DONE !!!','green'))
   else:
      parser.print_help()
if __name__ == '__main__':
  main()