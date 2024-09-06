import requests
import json
from bs4 import BeautifulSoup
import re

tech_count = 0


def fetch_web_content(domain):
    try:
        response = requests.get(f'https://{domain}')
        return response
    except requests.exceptions.RequestException as e:
        return None


def load_tech_footprints():
    with open('module/active/word_list/tech_pro5.json', 'r') as file:
        return json.load(file)


def detect(response, tech_footprints):
    global tech_count
    detected_technologies = []
    html_content = response.text
    headers = response.headers
    cookies = response.cookies.get_dict()
    soup = BeautifulSoup(html_content, 'html.parser')
    tech_range = len(tech_footprints)

    for tech in tech_footprints:
        tech_count += 1
        print(
            f"[{(tech_count/tech_range)*100:.2f}%][{tech_count}/{tech_range}]", end='\r')
        attributes = tech.get("attributes", {})
        html_patterns = attributes.get("html", [])
        if isinstance(html_patterns, str):
            html_patterns = [html_patterns]
        for pattern in html_patterns:
            try:
                if re.search(pattern, html_content):
                    detected_technologies.append(tech["name"])
                    break
            except re.error:
                pass

        header_patterns = attributes.get("headers", {})
        for header, pattern in header_patterns.items():
            try:
                if header in headers and re.search(pattern, headers[header]):
                    detected_technologies.append(tech["name"])
                    break
            except re.error:
                pass

        cookie_patterns = attributes.get("cookies", {})
        for cookie, pattern in cookie_patterns.items():
            try:
                if cookie in cookies and (not pattern or re.search(pattern, cookies[cookie])):
                    detected_technologies.append(tech["name"])
                    break
            except re.error:
                pass

        script_patterns = attributes.get("scripts", [])
        if isinstance(script_patterns, str):
            script_patterns = [script_patterns]
        for script in script_patterns:
            try:
                if re.search(script, html_content):
                    detected_technologies.append(tech["name"])
                    break
            except re.error:
                pass

        js_patterns = attributes.get("js", {})
        for js_var, pattern in js_patterns.items():
            try:
                if re.search(js_var, html_content):
                    if not pattern or re.search(pattern, html_content):
                        detected_technologies.append(tech["name"])
                        break
            except re.error:
                pass

        meta_patterns = attributes.get("meta", {})
        for meta_name, pattern in meta_patterns.items():
            try:
                meta_tag = soup.find('meta', attrs={"name": meta_name})
                if meta_tag and re.search(pattern, meta_tag.get("content", "")):
                    detected_technologies.append(tech["name"])
                    break
            except re.error:
                pass

        dom_patterns = attributes.get("dom", {})
        for selector, dom_attributes in dom_patterns.items():
            try:
                elements = soup.select(selector)
                for element in elements:
                    match = True
                    for attr_name, attr_value in dom_attributes.get("attributes", {}).items():
                        if not re.search(attr_value, element.get(attr_name, "")):
                            match = False
                            break
                    if match:
                        detected_technologies.append(tech["name"])
                        break
            except re.error:
                pass

        implied_techs = attributes.get("implies", [])
        if isinstance(implied_techs, str):
            implied_techs = [implied_techs]
        for implied_tech in implied_techs:
            detected_technologies.append(implied_tech)

    return list(set(detected_technologies))


def technology_pro5(domain, folder_result):
    web_content_sample = folder_result + f'/active/web_content.txt'
    technology_pro5_sample = folder_result + f'/active/technology_pro5.txt'
    response = fetch_web_content(domain)
    soup = BeautifulSoup(response.text, 'html.parser')
    html_content = str(soup)

    if response == None:
        with open(web_content_sample, 'w') as file:
            file.write('Error to download content and response headers')
        return

    with open(web_content_sample, 'w') as file:
        file.write(html_content)
    tech_footprints = load_tech_footprints()

    detected_technologies = detect(response, tech_footprints)
    with open(technology_pro5_sample, 'w') as file:
        for tech in detected_technologies:
            file.write(f'{tech}\n')