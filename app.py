from flask import Flask, request, jsonify, render_template_string
import requests, os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HARSHU UID GENERATER - DEBUG</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #fff;
            text-align: center;
            padding: 20px;
            min-height: 100vh;
        }
        h1 { color:#4f9cff; margin-bottom:20px; text-shadow:2px 2px 8px rgba(0,0,0,0.5); }
        form { margin:20px auto; padding:20px; background: rgba(255,255,255,0.07); border-radius:15px; box-shadow:0 4px 20px rgba(0,0,0,0.4); width:60%; }
        input { padding:12px; width:65%; border-radius:10px; border:none; outline:none; margin-right:10px; }
        button { padding:12px 20px; background:#4f9cff; color:#fff; border:none; border-radius:10px; cursor:pointer; font-weight:bold; transition:0.3s; }
        button:hover { background:#357ae8; }
        #loader { display:none; margin:20px auto; }
        .spinner { border:6px solid rgba(255,255,255,0.2); border-top:6px solid #4f9cff; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin:auto; }
        @keyframes spin {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}
        table { margin:30px auto; border-collapse: collapse; width:85%; background: rgba(255,255,255,0.05); border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.3);}
        th, td { padding:14px; border-bottom:1px solid rgba(255,255,255,0.1);}
        th { background: rgba(79,156,255,0.2); color:#4f9cff; font-size:18px; }
        tr:hover { background: rgba(255,255,255,0.08); }
        .copy-btn { background:#28a745; border:none; padding:6px 12px; border-radius:6px; color:white; font-size:13px; cursor:pointer;}
        .copy-btn:hover { background:#218838; }
        footer { margin-top:50px; font-size:14px; color:#aaa; }
        footer a { color:#4f9cff; text-decoration:none; font-weight:bold; }
        pre { text-align:left; background: rgba(0,0,0,0.4); padding:10px; border-radius:10px; overflow-x:auto;}
    </style>
</head>
<body>
    <h1>🔐 HARSHU UID GENERATER - DEBUG</h1>
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

    // Debug: Show full JSON
    let html = "<h2>Raw JSON Response:</h2><pre>"+JSON.stringify(data,null,2)+"</pre>";

    // If groups exist, show table
    if(data.data && data.data.length > 0){
        html += "<h2>Groups Table:</h2><table><tr><th>Group Name</th><th>Group ID</th><th>Action</th></tr>";
        data.data.forEach(g=>{
            html += `<tr>
                        <td>${g.name}</td>
                        <td id="gid-${g.id}">${g.id}</td>
                        <td><button class="copy-btn" onclick="copyId('${g.id}')">Copy</button></td>
                     </tr>`;
        });
        html += "</table>";
    }

    document.getElementById('output').innerHTML = html;
};

function copyId(id){
    navigator.clipboard.writeText(id).then(()=>{
        alert("Copied Group ID: " + id);
    });
}
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
        data = resp.json()
        print("DEBUG RESPONSE:", data)  # Console pe bhi output aayega
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
