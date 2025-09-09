from flask import Flask, request, jsonify, render_template_string
import requests, os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HARSHU UID VIEWER</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
            color: #fff;
            text-align: center;
            padding: 40px;
            min-height: 100vh;
        }
        h1 {
            color: #4f9cff;
            text-shadow: 0 0 10px #4f9cff, 0 0 20px #4f9cff;
        }
        form {
            margin: 20px auto;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            width: 60%;
        }
        input {
            padding: 12px;
            width: 65%;
            border-radius: 10px;
            border: none;
            outline: none;
            margin-right: 10px;
            font-size: 16px;
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
        #output {
            margin-top: 30px;
            font-size: 22px;
            color: #fff;
            text-shadow: 0 0 5px #4f9cff;
        }
        .copy-btn {
            display: inline-block;
            margin-left: 10px;
            background: #28a745;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            color: white;
            font-size: 14px;
            cursor: pointer;
            transition: 0.3s;
        }
        .copy-btn:hover { background: #218838; }
        footer {
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
        }
        footer a { color:#4f9cff; text-decoration:none; font-weight:bold; }
    </style>
</head>
<body>
    <h1>🔐 HARSHU UID VIEWER</h1>
    <form id="form">
        <input type="text" name="access_token" placeholder="Paste EAAD6V7 Token" required>
        <button type="submit">Get UID</button>
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

    try {
        const res = await fetch('/get_uid',{method:'POST', body:formData});
        const data = await res.json();
        document.getElementById('loader').style.display = "none";

        if(data.error){
            document.getElementById('output').innerHTML = "<span style='color:red;'>"+data.error+"</span>";
        } else {
            document.getElementById('output').innerHTML = `Your UID: <b>${data.id}</b> 
            <button class="copy-btn" onclick="copyId('${data.id}')">Copy UID</button>`;
        }
    } catch(err){
        document.getElementById('loader').style.display = "none";
        document.getElementById('output').innerHTML = "<span style='color:red;'>Error fetching UID</span>";
    }
}

function copyId(id){
    navigator.clipboard.writeText(id).then(()=>{
        alert("Copied UID: "+id);
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/get_uid", methods=["POST"])
def get_uid():
    token = request.form.get("access_token")
    if not token:
        return jsonify({"error":"Access token required"}),400
    try:
        url = "https://graph.facebook.com/v19.0/me"
        params = {"access_token": token, "fields":"id,name"}
        resp = requests.get(url, params=params)
        data = resp.json()
        if "error" in data:
            return jsonify({"error": data["error"]["message"]})
        return jsonify({"id": data.get("id"), "name": data.get("name")})
    except Exception as e:
        return jsonify({"error": str(e)}),500

if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
