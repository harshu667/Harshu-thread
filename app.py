from flask import Flask, request, jsonify
from flask import render_template_string
import requests

APP_TITLE = "HARSHU UID GENERATER"

app = Flask(__name__)

INDEX_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root{
      --bg:#0f1115; --card:#161a22; --muted:#9aa4b2; --text:#e6e8ec; --accent:#4f7cff;
      --ok:#21c55d; --bad:#ef4444; --ring:#2a3140;
    }
    *{box-sizing:border-box}
    body{margin:0; background:linear-gradient(180deg,#0f1115,#0b0d12 60%); color:var(--text); font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial}
    .wrap{max-width:940px; margin:40px auto; padding:0 16px}
    .card{background:var(--card); border:1px solid var(--ring); border-radius:18px; padding:18px; box-shadow:0 10px 30px rgba(0,0,0,.25)}
    h1{font-size:28px; margin:0 0 12px; letter-spacing:.5px}
    .subtitle{color:var(--muted); margin-bottom:18px}
    .row{display:flex; gap:12px; flex-wrap:wrap}
    input[type=text]{flex:1; padding:12px 14px; border-radius:12px; border:1px solid var(--ring); background:#0f1320; color:var(--text); outline:none}
    button{padding:12px 16px; border:0; border-radius:12px; background:var(--accent); color:#fff; font-weight:600; cursor:pointer}
    button:disabled{opacity:.6; cursor:not-allowed}
    .hint{color:var(--muted); font-size:13px; margin-top:8px}
    .status{margin-top:10px; font-size:14px}
    .status.ok{color:var(--ok)}
    .status.bad{color:var(--bad)}
    table{width:100%; border-collapse:collapse; margin-top:18px}
    th,td{padding:12px 10px; border-bottom:1px solid #232939; text-align:left; font-size:14px}
    th{color:#cdd6e5; font-weight:700}
    tbody tr:hover{background:#121623}
    .idchip{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; background:#0f1320; border:1px solid #222a3a; padding:4px 8px; border-radius:8px}
    .actions{display:flex; gap:8px; flex-wrap:wrap}
    .pill{padding:8px 10px; border-radius:10px; background:#1b2233; border:1px solid #2a3140; color:#cfe3ff; text-decoration:none; font-size:13px}
    .footer{margin-top:28px; color:var(--muted); font-size:14px; text-align:center}
    .grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:12px; margin-top:16px}
    .gcard{background:#121623; border:1px solid #202636; border-radius:14px; padding:12px}
    .gname{font-weight:700; margin:0 0 6px}
    .gmeta{font-size:13px; color:#a9b6cc}
    .copy{cursor:pointer}
    .badge{display:inline-block; padding:3px 8px; border-radius:999px; background:#1b2233; border:1px solid #2a3140; font-size:12px; color:#d9e5ff}
    .headerbar{display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:12px}
    .small{font-size:12px; color:#a0aaba}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="headerbar">
        <div>
          <h1>🔐 {{ title }}</h1>
          <div class="subtitle">Fetch your Facebook <b>Group IDs</b> safely using your own access token.</div>
        </div>
        <div class="badge">Live Demo</div>
      </div>

      <form id="tokenForm" class="row">
        <input type="text" name="access_token" id="access_token" placeholder="Paste your Access Token (EAAD6V7…)" required>
        <button id="btnFetch" type="submit">Get Groups</button>
      </form>
      <div class="hint">We never store your token. It’s posted only to your browser’s own server endpoint (<code>/get_groups</code>).</div>
      <div id="status" class="status"></div>

      <div id="summary" class="small" style="display:none; margin-top:12px;"></div>

      <div id="grid" class="grid" style="display:none;"></div>

      <table id="table" style="display:none;">
        <thead>
          <tr>
            <th style="width:40%">Group Name</th>
            <th>Group ID</th>
            <th>Members</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>

      <div class="footer">
        made by harshu with 💕 • contact me:
        <a class="pill" href="https://m.me/harshuuuxd" target="_blank" rel="noopener noreferrer">Messenger @harshuuuxd</a>
      </div>
    </div>
  </div>

<script>
const $ = (id)=>document.getElementById(id);

function setStatus(msg, ok=false, bad=false){
  const el = $("status");
  el.textContent = msg || "";
  el.className = "status" + (ok ? " ok" : bad ? " bad" : "");
}

function copyText(text){
  navigator.clipboard.writeText(text).then(()=> {
    setStatus("Copied: " + (text.length>20 ? text.slice(0,20)+"…" : text), true, false);
  }).catch(()=> setStatus("Copy failed", false, true));
}

function rowHTML(g){
  const gid = g.id || "";
  const gname = g.name || "(no name)";
  const members = g.member_count != null ? g.member_count : "—";
  const openUrl = "https://www.facebook.com/groups/" + encodeURIComponent(gid);
  return `
    <tr>
      <td>${gname}</td>
      <td><span class="idchip">${gid}</span></td>
      <td>${members}</td>
      <td class="actions">
        <a class="pill" href="${openUrl}" target="_blank" rel="noopener">Open</a>
        <a class="pill copy" onclick="copyText('${gid}')">Copy ID</a>
      </td>
    </tr>
  `;
}

function cardHTML(g){
  const gid = g.id || "";
  const gname = g.name || "(no name)";
  const members = g.member_count != null ? g.member_count : "—";
  const openUrl = "https://www.facebook.com/groups/" + encodeURIComponent(gid);
  return `
    <div class="gcard">
      <div class="gname">${gname}</div>
      <div class="gmeta">ID: <span class="idchip">${gid}</span></div>
      <div class="gmeta">Members: ${members}</div>
      <div class="actions" style="margin-top:10px">
        <a class="pill" href="${openUrl}" target="_blank" rel="noopener">Open</a>
        <a class="pill copy" onclick="copyText('${gid}')">Copy ID</a>
      </div>
    </div>
  `;
}

$("tokenForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const btn = $("btnFetch");
  const token = $("access_token").value.trim();
  if(!token){ setStatus("Please paste your access token.", false, true); return; }

  setStatus("Fetching your groups…");
  btn.disabled = true;

  try{
    const form = new FormData();
    form.append("access_token", token);
    const res = await fetch("/get_groups", { method:"POST", body: form });
    const data = await res.json();

    if(!res.ok){
      const err = (data && data.error && (data.error.message || data.error)) || "Unknown error";
      setStatus("Error: " + err, false, true);
      $("table").style.display="none";
      $("grid").style.display="none";
      $("summary").style.display="none";
      btn.disabled = false;
      return;
    }

    const groups = data.groups || [];
    if(groups.length === 0){
      setStatus("No groups found for this account/token.", false, true);
      $("table").style.display="none";
      $("grid").style.display="none";
      $("summary").style.display="none";
      btn.disabled = false;
      return;
    }

    // Summary
    $("summary").textContent = `Found ${groups.length} groups`;
    $("summary").style.display = "block";

    // Table
    $("tbody").innerHTML = groups.map(rowHTML).join("");
    $("table").style.display = "table";

    // Cards Grid
    $("grid").innerHTML = groups.map(cardHTML).join("");
    $("grid").style.display = "grid";

    setStatus("Success! Groups loaded.", true, false);
  }catch(err){
    setStatus("Request failed: " + (err?.message || err), false, true);
    $("table").style.display="none";
    $("grid").style.display="none";
    $("summary").style.display="none";
  }finally{
    btn.disabled = false;
  }
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML, title=APP_TITLE)

def fetch_all_groups(access_token: str, limit_per_page: int = 100):
    """
    Fetch all groups with pagination from Graph API v19.0.
    Only groups the user is a member of are returned by /me/groups.
    """
    url = "https://graph.facebook.com/v19.0/me/groups"
    params = {
        "access_token": access_token,
        "fields": "id,name,member_count",
        "limit": limit_per_page
    }
    all_items = []

    while True:
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()

        # API-level error
        if "error" in data:
            # propagate the full error payload back to caller
            raise ValueError(data["error"])

        items = data.get("data", [])
        all_items.extend(items)

        paging = data.get("paging", {})
        next_url = paging.get("next")
        if not next_url:
            break

        # Move to next page, reset params so requests won't merge
        url = next_url
        params = {}

    return all_items

@app.route("/get_groups", methods=["POST"])
def get_groups():
    access_token = request.form.get("access_token", "").strip()
    if not access_token:
        return jsonify({"error": "Access token is required"}), 400

    try:
        groups = fetch_all_groups(access_token)
        return jsonify({"groups": groups})
    except ValueError as api_err:
        # Graph API error object
        return jsonify({"error": api_err.args[0]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run locally in debug; do not use debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)
