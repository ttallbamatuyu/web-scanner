from flask import Flask, request, render_template_string, make_response, redirect
import time

app = Flask(__name__)

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
        <h2>1. Search (XSS Test)</h2>
        <form action="/search" method="GET">
            <input type="text" name="q" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
        {% if query %}
            <p>Results for: <strong style="color:red;">{{ query|safe }}</strong></p>
        {% endif %}
    </div>

    <div class="box">
        <h2>2. Network Diagnostic (CMDi Test)</h2>
        <form action="/ping" method="POST">
            <input type="text" name="ip" placeholder="8.8.8.8">
            <button type="submit">Ping Host</button>
        </form>
        {% if ping_result %}
            <pre style="background:#eee; padding:10px;">{{ ping_result }}</pre>
        {% endif %}
    </div>

    <div class="box">
        <h2>3. Image Fetcher (SSRF Test)</h2>
        <form action="/fetch" method="GET">
            <input type="text" name="url" placeholder="http://example.com/image.jpg">
            <button type="submit">Fetch Image</button>
        </form>
        {% if fetch_result %}
            <div style="background:#eee; padding:10px;">{{ fetch_result|safe }}</div>
        {% endif %}
    </div>

    <div class="box">
        <h2>4. Login (SQLi Test & Time-based Blind)</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
        {% if login_message %}
            <p style="color:blue;">{{ login_message }}</p>
        {% endif %}
    </div>
    
    <div class="box">
        <h2>5. File Reader (LFI Test)</h2>
        <form action="/read" method="GET">
            <input type="text" name="file" placeholder="test.txt">
            <button type="submit">Read File</button>
        </form>
        {% if file_content %}
            <pre style="background:#eee; padding:10px;">{{ file_content }}</pre>
        {% endif %}
    </div>

    <div class="box">
        <h2>6. Admin Area (Auth Test)</h2>
        {% if is_admin %}
            <p style="color:green;">Welcome Admin! You have an active session cookie.</p>
            <a href="/admin/secret">Access Secret Internal Metrics</a>
        {% else %}
            <p style="color:red;">Access Denied. Missing valid session cookie.</p>
        {% endif %}
    </div>

    <div class="box">
        <h2>7. Dynamic SPA Links (Playwright Crawler Test)</h2>
        <p>Links injected via JavaScript after 1 second.</p>
        <div id="dynamic-links"></div>
        <script>
            setTimeout(() => {
                document.getElementById('dynamic-links').innerHTML = '<a href="/hidden-api?action=delete">Hidden API Call</a>';
            }, 1000);
        </script>
    </div>
</body>
</html>
"""

def render_page(**kwargs):
    is_admin = request.cookies.get('session_id') == 'admin'
    return render_template_string(TEMPLATE, is_admin=is_admin, **kwargs)

@app.route('/', methods=['GET'])
def index():
    return render_page(query="")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    return render_page(query=query)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if "sleep(5)" in username.lower() or "waitfor delay" in username.lower():
        time.sleep(5)
        message = "Login failed."
    elif "' OR 1=1" in username or "' OR '1'='1" in username or username.endswith("' --"):
        message = f"Login Successful (Bypassed)! Executed mock query: SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    elif username == 'admin' and password == '1234':
        message = "Login Successful! Welcome, admin."
    else:
        message = "Invalid credentials."

    return render_page(query="", login_message=message)

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form.get('ip', '')
    result = ""
    if ip:
        if ';' in ip or '|' in ip or '&' in ip:
            result = f"PING {ip.split(';')[0]} (56 data bytes)\n"
            result += "64 bytes from ...\n\n"
            result += "[MOCK ROOT OS SHELL EXECUTED]\nroot:x:0:0:root:/root:/bin/bash\n"
        else:
            result = f"PING {ip} (56 data bytes)\n64 bytes from {ip}: icmp_seq=1 ttl=119 time=12.1 ms"
    return render_page(query="", ping_result=result)

@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url', '')
    result = ""
    if url:
        if "localhost" in url or "127.0.0.1" in url or "169.254" in url:
            result = f"<b>Successfully fetched internal resource:</b><br/><code>[INTERNAL_SECRET_DATA] Admin access token: SEC-99411-XYZ</code>"
        else:
            result = f"Fetched external URL: {url} (Simulated)"
    return render_page(query="", fetch_result=result)

@app.route('/read', methods=['GET'])
def read_file():
    file = request.args.get('file', '')
    content = "File not found."
    if "etc/passwd" in file.lower() or "win.ini" in file.lower():
        content = "[MOCK passwd file content]\nroot:x:0:0:root:/root:/bin/bash\n"
    elif file:
        content = f"Contents of {file}: ..."
    return render_page(file_content=content)

@app.route('/admin/secret', methods=['GET'])
def admin_secret():
    if request.cookies.get('session_id') == 'admin':
        return "Congrats! You accessed the secret area using the session cookie."
    return "Forbidden", 403

@app.route('/hidden-api', methods=['GET'])
def hidden_api():
    return "This was extracted by Playwright!"

@app.route('/.env', methods=['GET'])
def dot_env():
    return "DB_PASSWORD=supersecret\nSECRET_KEY=1234\nMOCK_ENV_DATA=true\n"

@app.route('/.git/config', methods=['GET'])
def git_config():
    return "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n"

if __name__ == '__main__':
    print("[*] Starting Vulnerable Dummy Server on http://0.0.0.0:5000/")
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
