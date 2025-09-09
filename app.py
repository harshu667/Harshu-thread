from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HARSHU UID GENERATER</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #fff;
            text-align: center;
            padding: 20px;
            min-height: 100vh;
        }
        h1 {
            color: #4f9cff;
            margin-bottom: 20px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        }
        form {
            margin: 20px auto;
            padding: 20px;
            background: rgba(255,255,255,0.07);
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            width: 60%;
        }
        input {
            padding: 12px;
            width: 65%;
            border-radius: 10px;
            border: none;
            outline: none;
            margin-right: 10px;
        }
        button {
            padding: 12px 20px;
            background: #4f9cff;
            color: #fff;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        button:hover {
            background: #357ae8;
        }
        #loader {
            display: none;
            margin: 20px auto;
        }
        .spinner {
            border: 6px solid rgba(255,255,255,0.2);
            border-top: 6px solid #4f9cff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg);}
            100% { transform: rotate(360deg);}
        }
        table {
            margin: 30px auto;
            border-collapse: collapse;
            width: 80%;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        th {
            background: rgba(79,156,255,0.2);
            color: #4f9cff;
            font-size: 18px;
        }
        tr:hover {
            background: rgba(255,255,255,0.08);
        }
        footer {
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
        }
        footer a {
            color: #4f9cff;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🔐 HARSHU UID GENERATER</h1>
    <form id="form">
        <input type="text" name="access_token" placeholder="Paste Access Token" required>
        <button type="submit">Get Groups</button>
    </form>

    <div id="loader"><div class="spinner"></div></div>
    <div id="output"></div>

    <footer>
        made by harshu with 💕 <br>
        <a href="https://m.me/harshuuuxd" target="_blank">Contact Me</a>
    </footer>

<script>
document.getElementById('form').onsubmit = async (e)=>{
    e.preventDefault();
    document.getElementById('loader').style.display = "block";
    document.getElementById('output').innerHTML = "";

    const formData = new FormData(e.target);
    const res = await fetch('/get_groups', {method:'POST', body:formData});
    const data = await res.json();

    document.getElementById('loader').style.display = "none";

    if(data.error){
        document.getElementById('output').innerHTML = "<p style='color:red;'>"+data.error+"</p>";
        return;
    }
    if(data.data && data.data.length > 0){
        let html = "<table><tr><th>Group Name</th><th>Group ID</th></tr>";
        data.data.forEach(g=>{
            html += `<tr><td>${g.name}</td><td>${g.id}</td></tr>`;
        });
        html += "</table>";
        document.getElementById('output').innerHTML = html;
    } else {
        document.getElementById('output').innerHTML = "<p>No groups found.</p>";
    }
};
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/get_groups", methods=["POST"])
def get_groups():
    token = request.form.get("access_token")
    if not token:
        return jsonify({"error": "Access token required"}), 400

    try:
        url = "https://graph.facebook.com/v19.0/me/groups"
        params = {"access_token": token, "fields": "id,name"}
        resp = requests.get(url, params=params)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
