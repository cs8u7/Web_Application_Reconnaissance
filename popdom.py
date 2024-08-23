import argparse
import sys
import re
from datetime import datetime
import os
import shutil

from module.endpoint import fetch_urls
from module.endpoint import hidden_and_document_endpoint
from module.domain import subdomain_discover
from module.dns import ip_dns_lookup

def main():
   parser = argparse.ArgumentParser(description="Automate Reconnaissance Tool")
   parser.add_argument('-u', type=str, help="URL of target web application.")
   args = parser.parse_args()

   if len(sys.argv) == 1:
      parser.print_help()
      sys.exit(1)

   url_pattern = re.compile(r'^((http|https):\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/\S*)?$')

   if args.u:
                                                                                      
      print(",-.----.       ,----..   ,-.----.                    ,----..             ____   ")
      print("\    /  \     /   /   \  \    /  \      ,---,       /   /   \          ,'  , `. ")
      print("|   :    \   /   .     : |   :    \   .'  .' `\    /   .     :      ,-+-,.' _ | ")
      print("|   |  .\ : .   /   ;.  \|   |  .\ :,---.'     \  .   /   ;.  \  ,-+-. ;   , || ")
      print(".   :  |: |.   ;   /  ` ;.   :  |: ||   |  .`\  |.   ;   /  ` ; ,--.'|'   |  ;| ")
      print("|   |   \ :;   |  ; \ ; ||   |   \ ::   : |  '  |;   |  ; \ ; ||   |  ,', |  ': ")
      print("|   : .   /|   :  | ; | '|   : .   /|   ' '  ;  :|   :  | ; | '|   | /  | |  || ")
      print(";   | |`-' .   |  ' ' ' :;   | |`-' '   | ;  .  |.   |  ' ' ' :'   | :  | :  |, ")
      print("|   | ;    '   ;  \; /  ||   | ;    |   | :  |  ''   ;  \; /  |;   . |  ; |--'  ")
      print(":   ' |     \   \  ',  / :   ' |    '   : | /  ;  \   \  ',  / |   : |  | ,     ")
      print(":   : :      ;   :    /  :   : :    |   | '` ,/    ;   :    /  |   : '  |/      ")
      print("|   | :       \   \ .'   |   | :    ;   :  .'       \   \ .'   ;   | |`-'       ")
      print("`---'.|        `---`     `---'.|    |   ,.'          `---`     |   ;/           ")
      print(" `---`                    `---`      '---'                      '---'           ")                                                                    
      print('--------------------------------------------------------------------------------')

      if url_pattern.match(args.u):

         print('[+] Create Sample Folder')
         date = datetime.now().date()
         folder_result = str(date) + '#' + args.u
         if os.path.exists(folder_result) and os.path.isdir(folder_result):
            shutil.rmtree(folder_result)
         os.makedirs(folder_result, exist_ok=True)
         
         # print('[+] Endpoint Discover')
         # endpoint_result = folder_result + '/' +folder_result + '@endpoint.txt'
         # with open(endpoint_result, 'w') as file:
         #    pass 
         # fetch_urls(args.u,endpoint_result)

         # print('[+] Subdomain Discover')
         # subdomain_discover(args.u,endpoint_result,folder_result)

         # print('[+] Hidden Endpoints & Document Filtering')
         # hidden_and_document_endpoint(endpoint_result,folder_result)

         print('[+] IP Lookup and Reverse DNS Lookup')
         ip_dns_lookup(args.u,folder_result)

if __name__ == '__main__':
  main()