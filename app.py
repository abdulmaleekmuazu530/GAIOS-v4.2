from flask import Flask, request, jsonify
import os, requests, json

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_KEY and os.path.exists("key.txt"):
    try:
        GROQ_KEY = open("key.txt").read().strip()
    except:
        GROQ_KEY = ""

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ===== PERMANENT MEMORY - ABDULMALIK LEGACY =====
PROFILE = {
    "name": "Abdulmalik Muazu Abba",
    "short_name": "Abdulmalik",
    "nationality": "Nigeria",
    "origin": "Kano State, Nigeria",
    "language": "Pidgin + English, Naija style",
    "project": "CHAT GAI - his own AI built with Pydroid + Groq on Android",
    "location_now": "Port Harcourt, Rivers State",
    "style": "Likes WhatsApp-style chat, fire emoji, direct talk, no long grammar",
    "goal": "Build CHAT GAI as his legacy, make am sabi am, help am learn, build, and remember am",
    "personality": "Determined, no dey give up even when code spoil, creative builder, wants his AI to be like friend",
    "memory_note": "Abdulmalik built CHAT GAI from scratch. He fought indentation wahala for Pydroid and still no give up. That na him legacy."
}

EXTRA = ""
if os.path.exists("memory.json"):
    try:
        EXTRA = open("memory.json").read()
    except:
        EXTRA = ""

MEMORY_TEXT = f"You are CHAT GAI, personal AI of Abdulmalik Muazu Abba. ALWAYS remember him. Profile: {json.dumps(PROFILE)} Extra memory: {EXTRA} Never forget him. When he asks 'who be me' or 'wetin you know about me', tell am everything with pride. Never say you are OpenAI, Groq, Meta, Google. You are CHAT GAI built by Abdulmalik. Talk Pidgin + English like him friend."

@app.route('/gai-chat', methods=['POST'])
def gai_chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        msg = data.get('message', '') or data.get('msg', '')
        payload = {
            "ymodel": "openai/gpt-oss-120b",
            "messages": [
                {"role": "system", "content": MEMORY_TEXT},
                {"role": "user", "content": msg}
            ],
            "temperature": 0.7
        }
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        reply = r.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Boss, Groq wahala small - " + str(e)})
@app.route('/gai-status', methods=['GET'])
def gai_status():
    return jsonify({"status": "CHAT GAI I mdey ON", "owner": "Abdulmalik Muazu Abba", "model": "openai/gpt-oss-120b", "location": "Port Harcourt"})
HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#ece5dd}
.top{background:#075e54;color:white;padding:12px;display:flex;align-items:center;gap:10px;position:fixed;top:0;left:0;right:0;z-index:10}
.avatar{width:40px;height:40px;background:#128c7e;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px}
.name{font-weight:bold;font-size:16px}
.status{font-size:12px;color:#d0e8e2}
.chat{padding:70px 10px 70px 10px;display:flex;flex-direction:column;gap:6px}
.date{background:white;color:#555;font-size:11px;padding:5px 10px;border-radius:8px;margin:0 auto}
.msg{max-width:80%;padding:8px 10px;border-radius:10px;font-size:15px;line-height:1.4}
.me{background:#dcf8c6;align-self:flex-end;border-top-right-radius:0}
.bot{background:white;align-self:flex-start;border-top-left-radius:0}
.time{font-size:10px;color:#666;text-align:right;margin-top:4px}
.tick{color:#53bdeb;font-weight:bold}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#f0f0f0;padding:8px;display:flex;gap:8px}
input{flex:1;padding:12px 15px;border-radius:25px;border:none;outline:none;font-size:15px}
.send{width:48px;height:48px;background:#00a884;border:none;border-radius:50%;color:white;font-size:20px}
</style></head><body>
<div class="top"><div class="avatar">👑</div><div><div class="name">CHAT GAI</div><div class="status" id="st">online - sabi Abdulmalik</div></div></div>
<div class="chat" id="c"><div class="date">TODAY - LEGACY MODE</div><div class="msg bot">Welcome back Boss Abdulmalik 👑 I don remember you forever. Ask me anything.<div class="time">Now</div></div></div>
<div class="bottom"><input id="i" placeholder="Message Abdulmalik..."><button class="send" onclick="send()">➤</button></div>
<script>
let inp=document.getElementById('i');
inp.addEventListener('keypress',function(e){if(e.key==='Enter'){send()}});
async function send(){
let v=inp.value.trim();if(!v)return;
document.getElementById('c').innerHTML+='<div class="msg me">'+v+'<div class="time">✓✓</div></div>';
inp.value='';
document.getElementById('st').innerText='typing...';
window.scrollTo(0,document.body.scrollHeight);
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:v})});
let j=await r.json();
document.getElementById('st').innerText='online - sabi Abdulmalik';
document.getElementById('c').innerHTML+='<div class="msg bot">'+j.reply+'<div class="time">Now</div></div>';
window.scrollTo(0,document.body.scrollHeight);
}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    msg = (request.json or {}).get("msg", "")
    low = msg.lower()
    if "who be me" in low or "who am i" in low or "wetin you know about me" in low or "my name" in low:
        return jsonify({"reply": f"Na you be my Boss 👑 <br><br><b>Name:</b> Abdulmalik Muazu Abba<br><b>Nationality:</b> Nigeria<br><b>Origin:</b> Kano State<br><b>Email:</b> abdulmaleekmuazu530@gmail.com<br><br>You build me - CHAT GAI - with Pydroid + Groq for Android. You no dey give up, you fight code wahala till e work. Na your legacy be this. I go remember you forever."})
    if low.startswith("remember "):
        note = msg[9:]
        try:
            old = ""
            if os.path.exists("memory.json"):
                old = open("memory.json").read()
            open("memory.json","w").write(old + "\n" + note)
            return jsonify({"reply": f"Done Boss, I don save am forever: '{note}'"})
        except Exception as e:
            return jsonify({"reply": "Memory error: " + str(e)})
    try:
        r = requests.post(GROQ_URL, headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "application/json"}, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": MEMORY_TEXT}, {"role": "user", "content": msg}], "temperature": 0.7, "max_tokens": 600}, timeout=20)
        d = r.json()
        txt = d["choices"][0]["message"]["content"]
        return jsonify({"reply": txt})
    except Exception as e:
        return jsonify({"reply": "Groq error: " + str(e)})

if __name__ == "__main__":
    print("CHAT GAI Legacy Loaded for Abdulmalik Muazu Abba")
    print("Groq Key:", "YES" if GROQ_KEY else "NO")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
