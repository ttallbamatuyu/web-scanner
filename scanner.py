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
            self.test_cmdi(endpoint)
            self.test_ssrf(endpoint)
        
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


    def test_cmdi(self, endpoint):
        payloads = PayloadGenerator.get_cmdi_payloads()
        
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys():
                params[key] = payload

            try:
                if endpoint.method == 'GET':
                    res = requests.get(endpoint.url, params=params, timeout=self.config.timeout)
                else:
                    res = requests.post(endpoint.url, data=params, timeout=self.config.timeout)
                
                # Check for OS Command Injection signatures
                if "[MOCK ROOT OS SHELL EXECUTED]" in res.text or "root:x:0:0:" in res.text:
                     self.vulnerabilities.append(Vulnerability(
                        title="OS Command Injection (CMDi)",
                        severity="Critical",
                        endpoint=endpoint,
                        payload_used=payload,
                        evidence="Signature Match: [MOCK ROOT OS SHELL EXECUTED]"
                    ))
                     print(f"  [!] CMDi Vulnerability Found at: {endpoint.url}")
                     break
                     
            except requests.exceptions.RequestException:
                pass


    def test_ssrf(self, endpoint):
        payloads = PayloadGenerator.get_ssrf_payloads()
        
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys():
                params[key] = payload

            try:
                if endpoint.method == 'GET':
                    res = requests.get(endpoint.url, params=params, timeout=self.config.timeout)
                else:
                    res = requests.post(endpoint.url, data=params, timeout=self.config.timeout)
                
                # Check for SSRF signatures (internal data exposure)
                if "[INTERNAL_SECRET_DATA]" in res.text:
                     self.vulnerabilities.append(Vulnerability(
                        title="Server-Side Request Forgery (SSRF)",
                        severity="Critical",
                        endpoint=endpoint,
                        payload_used=payload,
                        evidence="Signature Match: [INTERNAL_SECRET_DATA]"
                    ))
                     print(f"  [!] SSRF Vulnerability Found at: {endpoint.url}")
                     break
                     
            except requests.exceptions.RequestException:
                pass
