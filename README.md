# 🛡️ 웹 취약점 자동 진단 스캐너 (Automated Web Vulnerability Scanner)

이 프로젝트는 웹 애플리케이션에 존재하는 치명적인 보안 취약점들을 자동으로 탐지하고 진단하기 위해 파이썬(Python)으로 개발된 **화이트해커 교육 및 포트폴리오용 스캐너**입니다. 최신 버그바운티 트렌드를 반영하여 설계되었으며, 사용자가 직관적으로 진단 결과를 확인할 수 있도록 세련된 다크 모드 GUI와 자동화된 MS Word 보고서 생성 기능을 지원합니다.

---

## 🌟 주요 기능 (Key Features)

* **자동 공격 표면 수집 (Crawler Engine):** 타겟 URL을 순회하며 숨겨진 폼(Form)과 입력 파라미터를 식별합니다.
* **4대 핵심 취약점 점검 (Payload Engine):**
  1. **SQL Injection (SQLi):** 데이터베이스 쿼리 우회 시도
  2. **Cross-Site Scripting (XSS):** 악성 스크립트 반사(Reflected) 여부 확인
  3. **OS Command Injection (CMDi):** 서버 운영체제 명령어 실행 취약점 검증
  4. **Server-Side Request Forgery (SSRF):** 서버를 위조한 내부망 리소스 유출 검증
* **세련된 사용자 환경 (Modern GUI):** `customtkinter`를 활용한 다크 테마 데스크탑 앱 환경을 제공하여 터미널 없이도 클릭 한 번으로 점검을 수행할 수 있습니다.
* **진단 보고서 자동화 (Word Report):** 스캔이 종료되면 취약점의 종류, 심각도(Critical/High), 타겟 엔드포인트 및 증거(Evidence)가 정리된 `.docx` 보고서를 자동으로 생성하고 팝업으로 띄워줍니다.
* **안전한 모의 훈련 환경 제공:** 외부 사이트를 타격하지 않고 로컬에서 안전하게 원리를 학습할 수 있도록 의도적으로 취약하게 코딩된 자체 더미 서버(`dummy_server.py`)가 포함되어 있습니다.

---

## ⚙️ 기술 스택 (Tech Stack)

* **Language:** `Python 3.x`
* **HTTP/Parsing:** `requests`, `beautifulsoup4`
* **Desktop GUI:** `customtkinter`
* **Document Generator:** `python-docx`
* **Local Backend Framework:** `Flask`

---

## 🚀 사용 방법 (Getting Started)

파이썬 설치 유무와 관계없이, 누구나 쉽게 실행해 볼 수 있도록 독립 실행형 프로그램(`.exe`)으로 빌드되어 있습니다.

### 방법 1: 실행 파일(.exe)로 다이렉트 실행 (추천)
1. 프로젝트 폴더 내의 **`start_server.bat`** 파일을 더블 클릭하여 로컬 훈련용 더미 서버를 켭니다. (이 흑백 터미널 창은 끄지 말고 열어두세요)
2. **`dist/WebScanner.exe`** 프로그램을 더블 클릭하여 스캐너 앱을 실행합니다.
   > *참고: 개인이 직접 만든 프로그램이므로 Windows Defender 등 백신에서 경고가 나타날 수 있습니다. `추가 정보` -> `실행`을 누르시면 안전하게 켜집니다.*
3. 앱이 켜지면 **[Start Vulnerability Scan]** 버튼을 눌러 점검을 시작합니다!

### 방법 2: 파이썬(Python) 환경에서 직접 실행
개발자 환경에서 코드를 직접 돌려보고 싶으신 경우 아래 명령어를 사용하세요.

```bash
# 1. 필수 라이브러리 설치
pip install -r requirements.txt

# 2. 로컬 모의 타겟 서버 실행
python dummy_server.py

# 3. GUI 스캐너 앱 실행
python gui.py

# (선택) CLI 명령어 모드로 실행하고 싶다면
python main.py -t http://127.0.0.1:5000/ -o my_report.docx
```

---

## 🔒 법적 고지 및 윤리 규정 (Disclaimer)

**본 도구는 오직 교육, 연구, 그리고 지정된 모의 훈련 환경(`dummy_server.py`)에서의 사용을 목적으로 제작되었습니다.**  
사전 허가를 받지 않은 실제 서비스나 타인의 시스템, 서버를 대상으로 본 스캐너 엔진을 작동시키는 행위는 엄격히 금지됩니다. 본 프로그램의 오남용으로 인해 발생하는 모든 법적 문제와 피해에 대한 책임은 전적으로 사용자 본인에게 있습니다.
