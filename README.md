# 🛡️ 웹 취약점 자동 진단 스캐너 (Automated Web Vulnerability Scanner)

이 프로젝트는 웹 애플리케이션에 존재하는 치명적인 보안 취약점들을 자동으로 탐지하고 진단하기 위해 파이썬(Python)으로 개발된 **화이트해커 교육 및 포트폴리오용 스캐너**입니다. 최신 버그바운티 트렌드를 반영하여 설계되었으며, 사용자가 직관적으로 진단 결과를 확인할 수 있도록 세련된 다크 모드 GUI와 자동화된 MS Word 보고서 생성 기능을 지원합니다.

---

## 🌟 주요 기능 (Key Features)

### 🔍 동적 공격 표면 수집 (Playwright 기반 Headless 크롤러)
단순한 HTML 파싱을 넘어, **Headless Chromium 브라우저**를 통해 자바스크립트가 동적으로 렌더링하는 링크와 폼까지 모두 수집합니다. React/Vue 등 SPA 기반 웹에서도 숨겨진 엔드포인트를 발견할 수 있습니다.

### 🧪 7대 취약점 점검 모듈 (Payload Engine)
| # | 취약점 | CWE | CVSS | 탐지 방식 |
|---|---|---|---|---|
| 1 | SQL Injection (SQLi) | CWE-89 | 9.8 | 키워드 서명 기반 |
| 2 | **Time-Based Blind SQLi** | CWE-89 | 9.8 | 응답 지연 측정 |
| 3 | Cross-Site Scripting (XSS) | CWE-79 | 6.1 | 페이로드 반사 확인 |
| 4 | OS Command Injection (CMDi) | CWE-78 | 9.8 | 실행 결과 서명 기반 |
| 5 | Server-Side Request Forgery (SSRF) | CWE-918 | 8.6 | 내부망 응답 확인 |
| 6 | **Local File Inclusion (LFI)** | CWE-22 | 7.5 | 시스템 파일 내용 확인 |
| 7 | **Sensitive File Exposure** | CWE-200 | 5.3 | 비인가 파일 HTTP 200 확인 |

### 🔐 인증 기반 딥 스캐닝 (Cookie / Session 지원)
GUI의 'Cookies' 입력창에 `session_id=admin`처럼 세션 쿠키를 입력하면 로그인된 상태에서만 접근 가능한 인가된 영역까지 점검합니다.

### ⚡ 멀티스레딩 병렬 스캔 (Concurrent Engine)
`concurrent.futures.ThreadPoolExecutor`를 사용하여 지정한 스레드 수만큼 병렬로 페이로드를 전송합니다. 엔드포인트가 많아질수록 속도 차이가 극적으로 증가합니다.

### 📄 전문가급 보고서 자동 생성 (CWE/CVSS 통합 Word Report)
스캔 완료 시 **국제 표준 CWE 식별자**와 **CVSS v3 점수**, 해결 방안(Remediation)이 심각도별 색상(빨강/주황/노랑)과 함께 `.docx` 보고서로 자동 생성됩니다.

### 🖥️ 모던 다크 테마 GUI
`customtkinter` 기반 세련된 다크 테마 GUI에서 쿠키, 스레드 수, 리포트 파일명을 모두 클릭 한 번으로 설정하고 스캔할 수 있습니다.

---

## ⚙️ 기술 스택 (Tech Stack)

| 영역 | 라이브러리 |
|---|---|
| Language | `Python 3.10+` |
| Dynamic Crawler | `playwright` (Headless Chromium) |
| HTTP / Parsing | `requests`, `beautifulsoup4` |
| Desktop GUI | `customtkinter` |
| Document Generator | `python-docx` |
| Local Backend | `Flask` |
| Concurrency | `concurrent.futures` (Built-in) |

---

## 🚀 사용 방법 (Getting Started)

### 방법 1: 실행 파일(.exe)로 다이렉트 실행 (추천)
1. **`start_server.bat`** 파일을 더블 클릭하여 훈련용 더미 서버를 켭니다. (창을 닫지 마세요)
2. **`dist/WebScanner.exe`** 를 더블 클릭하여 스캐너 앱을 열어줍니다.
   > 참고: 개인 빌드 프로그램이므로 Windows Defender에서 경고가 뜰 수 있습니다. `추가 정보` → `실행`을 누르시면 됩니다.
3. GUI에서 필요 시 Cookie / Thread 수를 설정하고 **[Start Vulnerability Scan]** 버튼을 클릭하세요!

### 방법 2: 파이썬(Python) 환경에서 소스 코드 직접 실행

```bash
# 1. 필수 라이브러리 설치
pip install -r requirements.txt

# 2. Playwright 브라우저 엔진 설치 (최초 1회만)
python -m playwright install chromium

# 3. 로컬 모의 타겟 서버 실행
python dummy_server.py

# 4. GUI 스캐너 앱 실행
python gui.py

# (선택) CLI 명령어 모드로 실행
# -c 옵션으로 세션 쿠키 지정 가능
python main.py -t http://127.0.0.1:5000/ -o report.docx -c "session_id=admin" --threads 5
```

---

## 📁 프로젝트 구조 (Project Structure)

```
웹 스캐너/
├── gui.py            # 메인 GUI 앱 (진입점)
├── main.py           # CLI 진입점
├── crawler.py        # Playwright 기반 동적 크롤러
├── scanner.py        # 7대 취약점 탐지 엔진 (멀티스레딩)
├── reporter.py       # CWE/CVSS Word 보고서 생성기
├── payloads.py       # 공격 페이로드 데이터베이스
├── models.py         # 데이터 모델 (Vulnerability, Endpoint 등)
├── dummy_server.py   # 훈련/테스트용 취약 Flask 서버
├── start_server.bat  # 더미 서버 실행 스크립트
├── requirements.txt  # 파이썬 의존성 목록
└── dist/
    └── WebScanner.exe  # 빌드된 독립 실행 파일
```

---

## 🔒 법적 고지 및 윤리 규정 (Disclaimer)

**본 도구는 오직 교육, 연구, 그리고 지정된 모의 훈련 환경(`dummy_server.py`)에서의 사용을 목적으로 제작되었습니다.**  
사전 허가를 받지 않은 실제 서비스나 타인의 시스템, 서버를 대상으로 본 스캐너 엔진을 작동시키는 행위는 **엄격히 금지**됩니다. 본 프로그램의 오남용으로 인해 발생하는 모든 법적 문제와 피해에 대한 책임은 전적으로 사용자 본인에게 있습니다.
