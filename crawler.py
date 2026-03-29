import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models import Endpoint

class Crawler:
    def __init__(self, target_url):
        self.target_url = target_url
        self.endpoints = []

    def crawl(self):
        print(f"[*] Starting crawl on {self.target_url}")
        try:
            response = requests.get(self.target_url, timeout=5)
            self._parse_page(response.text, self.target_url)
        except requests.exceptions.RequestException as e:
            print(f"[!] Error crawling {self.target_url}: {e}")
        
        return self.endpoints

    def _parse_page(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Extract forms
        for form in soup.find_all('form'):
            action = form.get('action')
            method = form.get('method', 'get').upper()
            
            form_url = urljoin(url, action) if action else url
            
            inputs = {}
            for input_tag in form.find_all(['input', 'textarea']):
                name = input_tag.get('name')
                if name:
                    inputs[name] = "" # Default parameter value
            
            endpoint = Endpoint(url=form_url, method=method, parameters=inputs)
            self.endpoints.append(endpoint)
            print(f"[+] Found Attack Surface (Form): {method} {form_url} with params: {list(inputs.keys())}")

        # 2. Extract links (basic query parameter extraction, e.g., ?id=1)
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and '?' in href:
                link_url = urljoin(url, href)
                base_url, query_string = link_url.split('?', 1)
                
                params = {}
                for param in query_string.split('&'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        params[k] = v
                
                if params:
                    endpoint = Endpoint(url=base_url, method='GET', parameters=params)
                    self.endpoints.append(endpoint)
                    print(f"[+] Found Attack Surface (Link): GET {base_url} with params: {list(params.keys())}")
