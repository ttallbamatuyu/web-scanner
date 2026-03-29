import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from models import Endpoint

class Crawler:
    def __init__(self, target_url, cookies=None):
        self.target_url = target_url
        self.cookies = cookies or {}
        self.endpoints = []

    def _inject_cookies(self, context):
        if not self.cookies:
            return
        playwright_cookies = []
        domain = urlparse(self.target_url).hostname or "127.0.0.1"
        for k, v in self.cookies.items():
            playwright_cookies.append({
                "name": k,
                "value": v,
                "domain": domain,
                "path": "/"
            })
        context.add_cookies(playwright_cookies)

    def crawl(self):
        print(f"[*] Starting dynamic crawl on {self.target_url}")
        html = ""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                self._inject_cookies(context)
                
                page = context.new_page()
                page.goto(self.target_url, wait_until="networkidle")
                page.wait_for_timeout(2000)
                html = page.content()
                browser.close()
            print("[+] Dynamic JS rendering completed.")
        except Exception as e:
            print(f"[-] Playwright unavailable or failed, falling back to static requests: {e}")
            import requests
            headers = {"Cookie": "; ".join([f"{k}={v}" for k, v in self.cookies.items()])} if self.cookies else {}
            try:
                res = requests.get(self.target_url, headers=headers, timeout=5)
                html = res.text
            except Exception as e2:
                print(f"[!] Fallback error: {e2}")
                return self.endpoints

        self._parse_page(html, self.target_url)

        # Deduplicate
        seen = set()
        deduped = []
        for ep in self.endpoints:
            sig = f"{ep.method}_{ep.url}_{sorted(ep.parameters.keys())}"
            if sig not in seen:
                seen.add(sig)
                deduped.append(ep)
        self.endpoints = deduped
        return self.endpoints

    def _parse_page(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        for form in soup.find_all('form'):
            action = form.get('action')
            method = form.get('method', 'get').upper()
            form_url = urljoin(url, action) if action else url
            
            inputs = {}
            for input_tag in form.find_all(['input', 'textarea']):
                name = input_tag.get('name')
                if name:
                    inputs[name] = ""
            
            endpoint = Endpoint(url=form_url, method=method, parameters=inputs)
            self.endpoints.append(endpoint)
            print(f"[+] Found Attack Surface (Form): {method} {form_url} with params: {list(inputs.keys())}")

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and '?' in href:
                link_url = urljoin(url, href)
                base_url, query_string = link_url.split('?', 1)
                
                params = {}
                for param in query_string.split('&'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        if k:
                            params[k] = v
                
                if params:
                    endpoint = Endpoint(url=base_url, method='GET', parameters=params)
                    self.endpoints.append(endpoint)
                    print(f"[+] Found Attack Surface (Link): GET {base_url} with params: {list(params.keys())}")
