import sys
import os
import threading
import customtkinter as ctk
from datetime import datetime

# Import scanner components
from models import ScanConfig
from crawler import Crawler
from scanner import ScannerEngine
from reporter import Reporter

# --- Set CustomTkinter Appearance ---
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class TextRedirector:
    """Redirects console output (sys.stdout) to a CustomTkinter Textbox."""
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        self.textbox.insert("end", string)
        self.textbox.see("end")  # Auto-scroll to the bottom

    def flush(self):
        pass

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Web Vulnerability Scanner - White Hat Portfolio")
        self.geometry("900x600")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Push bottom elements down

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Vuln Scanner GUI", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Target input
        self.target_label = ctk.CTkLabel(self.sidebar_frame, text="Target URL:", font=ctk.CTkFont(size=14))
        self.target_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.target_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="http://127.0.0.1:5000/")
        self.target_entry.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.target_entry.insert(0, "http://127.0.0.1:5000/") # Default for local testing

        # Scan Button
        self.scan_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Start Vulnerability Scan", 
            command=self.start_scan_thread,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.scan_btn.grid(row=3, column=0, padx=20, pady=(10, 30))

        # Output file name
        self.output_label = ctk.CTkLabel(self.sidebar_frame, text="Report File Name (Word):", font=ctk.CTkFont(size=14))
        self.output_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.output_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="result.docx")
        self.output_entry.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.output_entry.insert(0, "result.docx")

        # --- Main Workspace ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Live Scan Engine Log", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Textbox for logs
        self.log_box = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=13))
        self.log_box.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Initial Welcome Message
        self.log_box.insert("end", "[*] System Ready. Awaiting target to initiate scan...\n")

        # Redirect standard output to the Textbox
        sys.stdout = TextRedirector(self.log_box)

    def start_scan_thread(self):
        # Prevent multiple clicks
        self.scan_btn.configure(state="disabled", text="Scanning in progress...")
        
        url = self.target_entry.get().strip()
        out_file = self.output_entry.get().strip()
        
        if not url:
            print("[!] Error: Target URL cannot be empty.")
            self.scan_btn.configure(state="normal", text="Start Vulnerability Scan")
            return
            
        if not url.startswith("http"):
             url = "http://" + url

        # Clear the log box
        self.log_box.delete("0.0", "end")

        # Run scan logic in background to keep GUI responsive
        threading.Thread(target=self.run_scan_logic, args=(url, out_file), daemon=True).start()

    def run_scan_logic(self, target_url, output_file):
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Launching Scanner Engine...")
            config = ScanConfig(target_url=target_url)

            # 1. Crawl
            crawler = Crawler(config.target_url)
            endpoints = crawler.crawl()

            # 2. Scan
            if endpoints:
                scanner = ScannerEngine(config)
                findings = scanner.run(endpoints)
                
                print("\n" + "="*50)
                print(f"[*] SCAN SUMMARY: Found {len(findings)} vulnerabilities")
                for f in findings:
                    print(f" - [{f.severity}] {f.title} @ {f.endpoint.url}")
                print("="*50)
                
                # 3. Report
                Reporter.generate_docx(findings, output_file=output_file)
                print(f"[+] Processing completed safely.")
                
                # Auto open the generated document
                try:
                    abs_path = os.path.abspath(output_file)
                    print(f"[*] Word report successfully assembled: {abs_path}")
                    print("[*] Automatically opening the report...")
                    # os.startfile is built-in on Windows systems
                    os.startfile(abs_path) 
                except Exception as e:
                    print(f"[!] Could not open the report automatically: {e}")
            else:
                print("[!] No endpoints discovered. Cannot proceed with scanning.")

        except Exception as e:
             print(f"\n[!] A fatal error occurred: {e}")
        finally:
            # Re-enable the button once complete
            self.scan_btn.configure(state="normal", text="Start Vulnerability Scan")


if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()
