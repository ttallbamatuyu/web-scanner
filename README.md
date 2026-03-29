# Automated Web Vulnerability Scanner 🛡️

A modern, Python-based web vulnerability scanning tool designed to automatically identify critical security flaws such as **SQL Injection** and **Reflected XSS** in web applications. This tool was built for educational purposes and to demonstrate core cybersecurity automation concepts as part of a White-Hat Hacker portfolio.

## 🌟 Key Features

* **Attack Surface Crawler:** Automatically navigates the target URL to extract form inputs, parameters, and actionable links.
* **Intelligent Payload Engine:** Injects customized, educational security payloads into discovered parameters.
* **Dual Interface (CLI & GUI):** 
  * A lightweight Command-Line Interface (`main.py`) for quick terminal-based testing.
  * A modern, sleek, dark-themed Desktop GUI (`gui.py`) built with `customtkinter`.
* **Automated Word Reporting:** Compiles the results (vulnerability type, severity, evidence, endpoints) into a beautifully formatted Microsoft Word (`.docx`) report.
* **Non-Blocking Architecture:** Uses Python `threading` to keep the UI fully responsive during long scanning tasks.
* **Dummy Target Server Included:** Comes with a built-in vulnerable Flask server (`dummy_server.py`) so you can safely test the tool locally.

## ⚙️ Built With

* Language: `Python 3.x`
* Networking/Parsing: `requests`, `beautifulsoup4`
* GUI Framework: `customtkinter`
* Reporting: `python-docx`
* Target Backend: `Flask`

---

## 🚀 Getting Started

### 1. Installation

Make sure you have Python 3.x installed on your system.
Install the required dependencies using pip:

```bash
pip install Flask requests beautifulsoup4 python-docx customtkinter
```
*(Optionally, you can install from the `requirements.txt` file if included: `pip install -r requirements.txt`)*

### 2. Running the Target (Dummy Server)

To test the scanner safely, start the local vulnerable testing server first. Open a terminal and run:

```bash
python dummy_server.py
```
*The server will start on `http://127.0.0.1:5000/`.*

### 3. Running the Scanner

You can run the scanner in either GUI or CLI mode.

#### Option A: Modern GUI Mode (Recommended)
Open a new terminal and run:
```bash
python gui.py
```
- A desktop window will appear.
- The `Target URL` is pre-filled with the local server address.
- Click **"Start Vulnerability Scan"**.
- Once the scan completes, your `.docx` report will automatically open!

#### Option B: CLI Mode
If you prefer running scans directly from the terminal:
```bash
python main.py -t http://127.0.0.1:5000/ -o my_report.docx
```

---

## 🔒 Legal & Ethical Disclaimer

**This tool is strictly for educational purposes and authorized auditing only.** 
Never use this tool to scan, crawl, or inject payloads into systems, applications, or servers that you do not have explicit permission to test. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.
