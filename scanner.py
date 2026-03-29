import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from models import Vulnerability, Endpoint
from payloads import PayloadGenerator

class ScannerEngine:
    def __init__(self, config):
        self.config = config
        self.vulnerabilities = []
        self.headers = {}
        if self.config.cookies:
            self.headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in self.config.cookies.items()])

    def run(self, endpoints):
        print(f"\n[*] Starting Scanner Engine on {len(endpoints)} endpoints with {self.config.threads} threads...")
        
        with ThreadPoolExecutor(max_workers=self.config.threads) as executor:
            for endpoint in endpoints:
                executor.submit(self.test_xss, endpoint)
                executor.submit(self.test_sqli, endpoint)
                executor.submit(self.test_time_sqli, endpoint)
                executor.submit(self.test_cmdi, endpoint)
                executor.submit(self.test_ssrf, endpoint)
                executor.submit(self.test_lfi, endpoint)
                
            if endpoints:
                base_url = f"{urlparse(endpoints[0].url).scheme}://{urlparse(endpoints[0].url).netloc}"
                executor.submit(self.test_sensitive_files, base_url)
                
        return self.vulnerabilities

    def _make_request(self, method, url, params=None, data=None):
        try:
            if method == 'GET':
                return requests.get(url, params=params, headers=self.headers, timeout=self.config.timeout)
            else:
                return requests.post(url, data=data, headers=self.headers, timeout=self.config.timeout)
        except requests.exceptions.RequestException:
            return None

    def test_xss(self, endpoint):
        payloads = PayloadGenerator.get_xss_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            
            if res and payload in res.text:
                self.vulnerabilities.append(Vulnerability(
                    title="Reflected XSS", severity="High", endpoint=endpoint, payload_used=payload,
                    evidence="Payload reflected successfully in response body.",
                    remediation="사용자 입력값을 신뢰하지 말고, 출력 시 반드시 HTML 엔티티로 이스케이프해야 합니다. 가능한 경우 CSP를 도입하세요.",
                    cwe="CWE-79", cvss_score=6.1
                ))
                print(f"  [!] XSS Vulnerability Found at: {endpoint.url}")
                break

    def test_sqli(self, endpoint):
        payloads = PayloadGenerator.get_sqli_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            
            indicators = ["Login Successful (Bypassed)", "Executed mock query", "syntax error"]
            evidence = None
            if res:
                for ind in indicators:
                    if ind.lower() in res.text.lower():
                        evidence = f"Signature Match: {ind}"
                        break
            if evidence:
                self.vulnerabilities.append(Vulnerability(
                    title="SQL Injection", severity="Critical", endpoint=endpoint, payload_used=payload,
                    evidence=evidence,
                    remediation="사용자 입력값을 직접 SQL 쿼리에 연결하지 말고, Prepared Statement를 사용하거나 안전한 ORM을 사용하세요.",
                    cwe="CWE-89", cvss_score=9.8
                ))
                print(f"  [!] SQLi Vulnerability Found at: {endpoint.url}")
                break

    def test_time_sqli(self, endpoint):
        payloads = PayloadGenerator.get_time_sqli_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            
            start_time = time.time()
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            elapsed = time.time() - start_time
            
            # If our sleep was 5s and the response took longer than 4.5s
            if res and elapsed > 4.5:
                self.vulnerabilities.append(Vulnerability(
                    title="Time-based Blind SQL Injection", severity="Critical", endpoint=endpoint, payload_used=payload,
                    evidence=f"Response delayed by {elapsed:.2f} seconds.",
                    remediation="네트워크 지연 유발 함수를 악용할 수 없도록 Prepared Statement를 강제 적용하세요.",
                    cwe="CWE-89", cvss_score=9.8
                ))
                print(f"  [!] Time-Blind SQLi Found at: {endpoint.url} with {elapsed:.2f}s delay")
                break

    def test_cmdi(self, endpoint):
        payloads = PayloadGenerator.get_cmdi_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            
            if res and ("[MOCK ROOT OS SHELL EXECUTED]" in res.text or "root:x:0:0:" in res.text):
                self.vulnerabilities.append(Vulnerability(
                    title="OS Command Injection (CMDi)", severity="Critical", endpoint=endpoint, payload_used=payload,
                    evidence="Signature Match: [MOCK ROOT OS SHELL EXECUTED]",
                    remediation="운영체제 명령어의 직접적인 호출을 피하고, 불가피한 경우 입력값을 엄격한 화이트리스트로 검증하세요.",
                    cwe="CWE-78", cvss_score=9.8
                ))
                print(f"  [!] CMDi Vulnerability Found at: {endpoint.url}")
                break

    def test_ssrf(self, endpoint):
        payloads = PayloadGenerator.get_ssrf_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            
            if res and "[INTERNAL_SECRET_DATA]" in res.text:
                self.vulnerabilities.append(Vulnerability(
                    title="Server-Side Request Forgery (SSRF)", severity="Critical", endpoint=endpoint, payload_used=payload,
                    evidence="Signature Match: [INTERNAL_SECRET_DATA]",
                    remediation="허용된 도메인/IP 주소 목록(화이트리스트)과 일치하는지 확인하고, 내부망 접근을 차단하세요.",
                    cwe="CWE-918", cvss_score=8.6
                ))
                print(f"  [!] SSRF Vulnerability Found at: {endpoint.url}")
                break

    def test_lfi(self, endpoint):
        payloads = PayloadGenerator.get_lfi_payloads()
        for payload in payloads:
            params = endpoint.parameters.copy()
            for key in params.keys(): params[key] = payload
            res = self._make_request(endpoint.method, endpoint.url, params if endpoint.method == 'GET' else None, params if endpoint.method != 'GET' else None)
            
            if res and ("root:x:0:0" in res.text or "[MOCK passwd file content]" in res.text or "[fonts]" in res.text):
                self.vulnerabilities.append(Vulnerability(
                    title="Local File Inclusion (LFI)", severity="High", endpoint=endpoint, payload_used=payload,
                    evidence="System file contents (e.g. /etc/passwd or win.ini) were successfully read.",
                    remediation="파일 경로를 사용자 입력으로 직접 구성하지 말고, 사전에 정의된 파일명 목록을 사용하세요.",
                    cwe="CWE-22", cvss_score=7.5
                ))
                print(f"  [!] LFI Vulnerability Found at: {endpoint.url}")
                break

    def test_sensitive_files(self, base_url):
        payloads = PayloadGenerator.get_sensitive_files()
        for path in payloads:
            target_url = urljoin(base_url, path)
            res = self._make_request('GET', target_url)
            
            # simple check if HTTP 200 and some sensitive keywords match
            if res and res.status_code == 200:
                is_sensitive = False
                if '/.env' in path and ('DB_PASSWORD' in res.text or 'SECRET_KEY' in res.text or 'MOCK_ENV_DATA' in res.text): is_sensitive = True
                if '/.git/config' in path and '[core]' in res.text: is_sensitive = True
                
                if is_sensitive:
                    self.vulnerabilities.append(Vulnerability(
                        title="Sensitive File Exposure", severity="High", endpoint=Endpoint(target_url, 'GET'), payload_used=path,
                        evidence="File fetched successfully with HTTP 200.",
                        remediation="중요 파일 및 디렉토리에 대한 웹 서버 접근 권한을 차단하세요.",
                        cwe="CWE-200", cvss_score=5.3
                    ))
                    print(f"  [!] Sensitive File Found at: {target_url}")
