import argparse
from models import ScanConfig
from crawler import Crawler
from scanner import ScannerEngine
from reporter import Reporter

def print_banner():
    banner = """
    =============================================
         Automated Web Vulnerability Scanner     
         (White-Hat Educational Portfolio)        
    =============================================
    """
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Web Vulnerability Scanner Engine")
    parser.add_argument("-t", "--url", required=True, help="Target URL (e.g., http://127.0.0.1:5000/)")
    parser.add_argument("-o", "--output", default="vulnerability_report.docx", help="Output Word document file name")
    parser.add_argument("-c", "--cookies", default="", help="Cookies e.g., session_id=admin")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads")
    args = parser.parse_args()

    target_url = args.url
    if not target_url.startswith('http'):
        target_url = "http://" + target_url

    cookies_dict = {}
    if args.cookies:
        for item in args.cookies.split(';'):
            if '=' in item:
                k, v = item.split('=', 1)
                cookies_dict[k.strip()] = v.strip()

    # 1. 스캔 설정 (Scan config setup)
    config = ScanConfig(target_url=target_url, cookies=cookies_dict, threads=args.threads)

    # 2. 크롤링 엔진 시작 (Discovery)
    crawler = Crawler(config.target_url, cookies=cookies_dict)
    endpoints = crawler.crawl()

    # 3. 발견된 엔드포인트 목록이 있다면 스캐닝 진행
    if endpoints:
        scanner = ScannerEngine(config)
        findings = scanner.run(endpoints)
        
        # 4. 결과 출력
        print("\n" + "="*50)
        print(f"[*] SCAN SUMMARY: Found {len(findings)} vulnerabilities")
        for f in findings:
            print(f" - [{f.severity}] {f.title} @ {f.endpoint.url}")
        print("="*50)
            
        # 5. Word 형태의 보고서 생성 (Generate docx report)
        Reporter.generate_docx(findings, output_file=args.output)
    else:
        print("[!] No endpoints discovered. Cannot proceed with scanning.")

if __name__ == "__main__":
    main()
