import requests
from models import Vulnerability
from payloads import PayloadGenerator

class ScannerEngine:
    def __init__(self, config):
        self.config = config
        self.vulnerabilities = []

    def run(self, endpoints):
        print(f"\n[*] Starting Scanner Engine on {len(endpoints)} endpoints...")
        for endpoint in endpoints:
            self.test_xss(endpoint)
            self.test_sqli(endpoint)
        
        return self.vulnerabilities

    def test_xss(self, endpoint):
        payloads = PayloadGenerator.get_xss_payloads()
        
        for payload in payloads:
            # Create a copy of parameters to inject payload
            params = endpoint.parameters.copy()
            for key in params.keys():
                params[key] = payload

            try:
                if endpoint.method == 'GET':
                    res = requests.get(endpoint.url, params=params, timeout=self.config.timeout)
                else:
                    res = requests.post(endpoint.url, data=params, timeout=self.config.timeout)
                    
                # Basic XSS check: is the unescaped payload directly present in the returned HTML?
                if payload in res.text:
                    self.vulnerabilities.append(Vulnerability(
                        title="Reflected XSS",
                        severity="High",
                        endpoint=endpoint,
                        payload_used=payload,
                        evidence=f"Payload reflected successfully in response body."
                    ))
                    print(f"  [!] XSS Vulnerability Found at: {endpoint.url}")
                    break # Stop testing local parameters on success to avoid duplicates
            except requests.exceptions.RequestException:
                pass


    def test_sqli(self, endpoint):
        payloads = PayloadGenerator.get_sqli_payloads()
        
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys():
                params[key] = payload

            try:
                if endpoint.method == 'GET':
                    res = requests.get(endpoint.url, params=params, timeout=self.config.timeout)
                else:
                    res = requests.post(endpoint.url, data=params, timeout=self.config.timeout)
                
                # Check for SQL bypassing or syntax errors in the dummy app
                indicators = ["Login Successful (Bypassed)", "Executed mock query", "syntax error"]
                
                evidence = None
                for indicator in indicators:
                    if indicator.lower() in res.text.lower():
                        evidence = f"Signature Match: {indicator}"
                        break
                        
                if evidence:
                     self.vulnerabilities.append(Vulnerability(
                        title="SQL Injection",
                        severity="Critical",
                        endpoint=endpoint,
                        payload_used=payload,
                        evidence=evidence
                    ))
                     print(f"  [!] SQL Injection Vulnerability Found at: {endpoint.url}")
                     break
                     
            except requests.exceptions.RequestException:
                pass
