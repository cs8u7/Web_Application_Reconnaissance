import requests
import json
from bs4 import BeautifulSoup
import re
import time
import os


def fetch_web_content(domain):
    try:
        response = requests.get(f'https://{domain}', timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None


def load_tech_footprints():
    with open('module/active/word_list/tech_pro5.json', 'r') as file:
        return json.load(file)


def detect_relative(detected_technologies, tech, technique):
    implied_techs = tech.get("attributes", {}).get("implies", [])

    if isinstance(implied_techs, str):
        implied_techs = [implied_techs]
    detected_technologies.extend(implied_techs)

    detected_technologies.append(f'{tech["name"]} - {technique}')

    return detected_technologies


def detect(response, tech_footprints):
    tech_count = 0
    detected_technologies = []
    html_content = response.text
    headers = response.headers.items()
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
                if re.search(html_content, pattern) or re.search(pattern, html_content):
                    detected_technologies = detect_relative(
                        detected_technologies, tech, 'HTML content')
                    break
            except re.error:
                pass

        header_patterns = tech.get("attributes", {}).get("headers", {})
        for header, pattern in header_patterns.items():
            for header_res, pattern_res in headers:
                if not pattern and header.lower() == header_res.lower():
                    detected_technologies = detect_relative(
                        detected_technologies, tech, 'HTTP headers')
                    break

                elif pattern and header.lower() == header_res.lower():
                    try:
                        if re.search(pattern_res, pattern) or re.search(pattern, pattern_res):
                            detected_technologies = detect_relative(
                                detected_technologies, tech, 'HTTP headers')
                            break
                    except re.error:
                        pass

        cookie_patterns = tech.get("attributes", {}).get("cookies", {})
        for cookie in cookie_patterns.keys():
            if cookie in cookies.keys():
                detected_technologies = detect_relative(
                    detected_technologies, tech, 'HTTP Cookie')
                break

        script_patterns = attributes.get("scripts", [])
        if isinstance(script_patterns, str):
            script_patterns = [script_patterns]

        script_tags = soup.find_all('script')

        for script in script_patterns:
            for script_tag in script_tags:
                try:
                    escaped_script = re.escape(script)
                    escaped_script_tag = re.escape(str(script_tag))
                    if re.search(escaped_script, escaped_script_tag) or re.search(escaped_script_tag, escaped_script):
                        detected_technologies = detect_relative(
                            detected_technologies, tech, 'HTML script tag')
                        break
                except re.error:
                    pass

        js_patterns = attributes.get("js", {})
        for js_var, pattern in js_patterns.items():
            try:
                if re.search(js_var, html_content):
                    if not pattern or re.search(html_content, pattern) or re.search(pattern, html_content):
                        detected_technologies = detect_relative(
                            detected_technologies, tech, 'js')
                        break
            except re.error:
                pass

        meta_patterns = attributes.get("meta", {})
        for meta_name, pattern in meta_patterns.items():
            meta_tags = soup.find_all('meta', attrs={"name": meta_name})
            for meta_tag in meta_tags:
                try:
                    if re.search(pattern, meta_tag.get("content", "")) or re.search(meta_tag.get("content", ""), pattern):
                        implied_techs = tech.get(
                            "attributes", {}).get("implies", [])

                        if isinstance(implied_techs, str):
                            implied_techs = [implied_techs]
                        detected_technologies.extend(implied_techs)

                        detected_technologies.append(
                            f'{meta_tag.get("content", "")} - meta')
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
                        if not re.search(element.get(attr_name, ""), attr_value):
                            match = False
                            break
                    if match:
                        detected_technologies = detect_relative(
                            detected_technologies, tech, 'DOM')
                        break
            except re.error:
                pass

    return detected_technologies


def technology_pro5(folder_result):
    start_time = time.time()
    subdomain_sample = folder_result + '/active/subdomain.txt'

    with open(subdomain_sample, 'r') as file:
        domains = file.read().splitlines()

    tech_footprints = load_tech_footprints()

    os.makedirs(f'{folder_result}/active/web_content/')
    os.makedirs(f'{folder_result}/active/technology_pro5/')

    for domain in domains:
        web_content_sample = folder_result + \
            f'/active/web_content/{domain}.txt'
        technology_pro5_sample = folder_result + \
            f'/active/technology_pro5/{domain}.txt'

        response = fetch_web_content(domain)

        if response is None:
            with open(web_content_sample, 'w') as file:
                file.write('Error to download content and response headers')
            break

        print(f'[-] Analyzing Web Content of {domain}')
        soup = BeautifulSoup(response.text, 'html.parser')
        html_content = str(soup)

        with open(web_content_sample, 'w') as file:
            file.write(html_content)
        
        detected_technologies = detect(response, tech_footprints)
        with open(technology_pro5_sample, 'w') as file:
            for tech in detected_technologies:
                file.write(f'{tech}\n')

        with open(technology_pro5_sample, 'r') as file:
            lines = file.readlines()
        unique_lines = sorted(set(lines))
        with open(technology_pro5_sample, 'w') as file:
            file.writelines(unique_lines)

    end_time = time.time()
    running = end_time - start_time
    print(f"\n[Time]: {running:.2f}s")
