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

if __name__ == '__main__':
    print("[*] Starting Vulnerable Dummy Server on http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', debug=True, port=5000)
