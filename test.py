import re
import requests
from bs4 import BeautifulSoup

def extract_ga_ids(domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    url=f'https://{domain}'
    session = requests.Session()
    request = requests.Request('GET', url, headers=headers)
    prepared_request = session.prepare_request(request)

    response = session.send(prepared_request)
    content = response.text

    ua_pattern = r'UA-\d{4,9}'
    ua_ids = re.findall(ua_pattern, content)
    
    return ua_ids

if __name__ == "__main__":
    domain = "https://blog.pocketcasts.com/"  # Replace with the target URL
    ga_ids = extract_ga_ids(domain)
    print("Extracted Google Analytics IDs:", ga_ids)
