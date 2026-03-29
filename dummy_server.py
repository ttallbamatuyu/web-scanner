from flask import Flask, request, render_template_string

app = Flask(__name__)

# Very simple HTML template for the dummy server apps
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Target Apps</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        .box { border: 1px solid #ccc; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Welcome to the Vulnerable Test Server</h1>
    
    <div class="box">
        <h2>Search (XSS Test)</h2>
        <form action="/search" method="GET">
            <input type="text" name="q" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
        {% if query %}
            <p>Results for: <strong style="color:red;">{{ query|safe }}</strong></p> <!-- VULNERABILITY: User input is NOT escaped -->
        {% endif %}
    </div>

    <div class="box">
        <h2>Network Diagnostic (CMDi Test)</h2>
        <form action="/ping" method="POST">
            <input type="text" name="ip" placeholder="8.8.8.8">
            <button type="submit">Ping Host</button>
        </form>
        {% if ping_result %}
            <pre style="background:#eee; padding:10px;">{{ ping_result }}</pre>
        {% endif %}
    </div>

    <div class="box">
        <h2>Image Fetcher (SSRF Test)</h2>
        <form action="/fetch" method="GET">
            <input type="text" name="url" placeholder="http://example.com/image.jpg">
            <button type="submit">Fetch Image</button>
        </form>
        {% if fetch_result %}
            <div style="background:#eee; padding:10px;">{{ fetch_result|safe }}</div>
        {% endif %}
    </div>

    <div class="box">
        <h2>Login (SQLi Test)</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
        {% if login_message %}
            <p style="color:blue;">{{ login_message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(TEMPLATE, query="")

@app.route('/search', methods=['GET'])
def search():
    # Intentionally vulnerable to Reflected XSS
    query = request.args.get('q', '')
    return render_template_string(TEMPLATE, query=query)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Intentionally vulnerable to SQL Injection (mock implementation)
    # Simulator checks if typical SQL bypass payloads are used.
    if "' OR 1=1" in username or "' OR '1'='1" in username or username.endswith("' --"):
        message = f"Login Successful (Bypassed)! Executed mock query: SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    elif username == 'admin' and password == '1234':
        message = "Login Successful! Welcome, admin."
    else:
        message = "Invalid credentials."

    return render_template_string(TEMPLATE, query="", login_message=message)

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form.get('ip', '')
    result = ""
    if ip:
        # Mocking OS Command Injection vulnerability
        if ';' in ip or '|' in ip or '&' in ip:
            result = f"PING {ip.split(';')[0]} (56 data bytes)\n"
            result += "64 bytes from ...\n\n"
            result += "[MOCK ROOT OS SHELL EXECUTED]\nroot:x:0:0:root:/root:/bin/bash\n"
        else:
            result = f"PING {ip} (56 data bytes)\n64 bytes from {ip}: icmp_seq=1 ttl=119 time=12.1 ms"
            
    return render_template_string(TEMPLATE, query="", ping_result=result)

@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url', '')
    result = ""
    if url:
        # Mocking Server-Side Request Forgery vulnerability
        if "localhost" in url or "127.0.0.1" in url or "169.254" in url:
            result = f"<b>Successfully fetched internal resource:</b><br/><code>[INTERNAL_SECRET_DATA] Admin access token: SEC-99411-XYZ</code>"
        else:
            result = f"Fetched external URL: {url} (Simulated)"
            
    return render_template_string(TEMPLATE, query="", fetch_result=result)

if __name__ == '__main__':
    print("[*] Starting Vulnerable Dummy Server on http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', debug=True, port=5000)
