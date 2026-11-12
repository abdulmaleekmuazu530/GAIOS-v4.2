from flask import Flask, request, jsonify, render_template
import os, requests, json
from datetime import datetime

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

# ===== GAIOS CONFIG =====
OWNER_PHONE = "+234 812 152 1859"
OWNER_NOTE = "Text Only, No Calls"
BRAND = "GAIOS"
WATERMARK = "Made by GAIOS"
OWNER_PASSWORD = "Amleek@900"

PROFILE = {
    "name": "Abdulmalik Muazu Abba",
    "short_name": "Abdulmalik",
    "nationality": "Nigeria",
    "origin": "Kano State, Nigeria",
    "language": "Pidgin + English, Naija style",
    "project": "CHAT GAI / GAIOS - his own AI built with Pydroid + Groq on Android",
    "location_now": "Port Harcourt, Rivers State",
    "style": "Likes WhatsApp-style chat, fire emoji, direct talk, no long grammar",
    "goal": "Build CHAT GAI as his legacy, make am sabi am, help am learn, build, and remember am",
    "personality": "Determined, no dey give up even when code spoil, creative builder, wants his AI to be like friend",
    "memory_note": "Abdulmalik built CHAT GAI from scratch. He fought indentation wahala for Pydroid and still no give up. That na him legacy.",
    "contact": OWNER_PHONE,
    "brand": BRAND
}

THEMES = {
    "default": {"name": "GAIOS Default", "colors": "Dark Blue + Gold"},
    "independence": {"name": "Nigeria Independence Day", "colors": "Green + White", "date": "10-01"},
    "sallah": {"name": "Sallah Day - Eid", "colors": "Green + Gold, Moon + Star"},
    "ramadan": {"name": "Ramadan", "colors": "Dark Purple + Gold, Lantern"},
    "christmas": {"name": "Christmas", "colors": "Red + White + Gold", "date": "12-25"},
    "newyear": {"name": "New Year", "colors": "Black + Gold Fireworks", "date": "01-01"},
    "valentine": {"name": "Valentine", "colors": "Red + Pink", "date": "02-14"},
    "childrens": {"name": "Children's Day", "colors": "Colourful", "date": "05-27"},
    "lagos": {"name": "Lagos Vibes", "colors": "Yellow + Black", "auto_day": "Friday"},
    "premium": {"name": "Premium Boss", "colors": "Black + Gold"}
}

STICKER_CATEGORIES = [
    "Naija Vibes", "Love & Romance", "Sallah & Ramadan", "Business & Money",
    "Motivation", "Funny & Meme", "Birthday", "Football", "Church & Gospel", "Premium Boss"
]

def load_json(fname, default):
    if os.path.exists(fname):
        try:
            return json.load(open(fname))
        except:
            return default
    return default

def save_json(fname, data):
    try:
        json.dump(data, open(fname, "w"), indent=2)
    except:
        pass

def is_owner(data):
    # NEW: password check + old checks
    return data.get("password") == OWNER_PASSWORD or data.get("owner_password") == OWNER_PASSWORD or data.get("owner_phone") == OWNER_PHONE or data.get("owner_code") == "GAIOS-OWNER" or data.get("is_owner") == True

def get_auto_theme():
    today = datetime.now()
    md = today.strftime("%m-%d")
    weekday = today.strftime("%A")
    for key, t in THEMES.items():
        if t.get("date") == md:
            return key
    if weekday == "Friday":
        return "lagos"
    return "default"

EXTRA = ""
if os.path.exists("memory.json"):
    try:
        EXTRA = open("memory.json").read()
    except:
        EXTRA = ""

GAIOS_SYSTEM = f"""
You are CHAT GAI / GAIOS, personal AI of Abdulmalik Muazu Abba. ALWAYS remember him.
Profile: {json.dumps(PROFILE)} Extra memory: {EXTRA}
Never say you are OpenAI, Groq, Meta, Google. You are CHAT GAI built by Abdulmalik.
Talk Pidgin + English like his friend. Pure English for business/status content when asked.

GAIOS FEATURES YOU MUST USE:
1. Memory System - Remember name, business, customers forever. Save to memory.json.
2. Business Partner Mode - Help with business plans, prices, proposals. Track sales, customers, ideas. Remind tasks. Goals: A) Sell 50 sticker packs/week B) Get 10 App Builder customers C) Open Drawing + Book Store.
3. Shop System - Drawing Store and Book Store inside app. Browse, order, pay. Add drawings/books anytime.
4. Status & Content Creator - WhatsApp status, captions, posters, announcements in pure English, in his style.
5. Voice Mode - User can talk, you talk back.
6. Group Mode - Join WhatsApp group, answer questions, remind members.
7. Owner Mode - Only Abdulmalik can control GAI, change settings, add features, see private info. Owner Phone: {OWNER_PHONE} - Text Only, No Calls.
8. Learning Mode - Learn from him every day, become smarter for his life/business.
9. Multi-Language Mode - Default pure English for business, Pidgin+English for chat, Hausa/Pidgin in Owner Mode if asked.
10. Offline Notes - Save important notes even without internet.
11. Page Themes - 10 themes: default, independence, sallah, ramadan, christmas, newyear, valentine, childrens, lagos, premium. Auto Theme Change ON. Owner can say 'Owner Mode: Change theme to Sallah Day'.
12. Sticker Maker - Create stickers with GAIOS watermark, Premium + Cute styles. Categories: {', '.join(STICKER_CATEGORIES)}
Contact for customers: {OWNER_PHONE} - Text Only, No Calls. Watermark: Made by GAIOS.
When he asks 'who be me' tell everything with pride.
PRIVACY RULE: Normal users see only chat. No buttons, no settings. Only Owner can change anything.
"""

MEMORY_TEXT = GAIOS_SYSTEM

# ===== FRONTEND - NO BUTTONS FOR USERS =====
@app.route("/app")
def app_page():
    return render_template("index.html")

@app.route("/")
def home():
    return jsonify({"status": "CHAT GAI / GAIOS V5.0 ONLINE", "owner": "Abdulmalik Muazu Abba", "features": ["Memory", "Business Partner", "Shop", "Status Creator", "Voice", "Group", "Owner Mode", "Learning", "Multi-Language", "Offline Notes", "10 Themes + Auto Change", "Sticker Maker", "Image/Voice/Clip Upload"], "contact": OWNER_PHONE, "app": "/app - Open this for chat"})

# ===== OWNER LOGIN - NEW - LONG PRESS LOGO 10 SEC =====
@app.route("/gai-owner-login", methods=["POST"])
def gai_owner_login():
    data = request.get_json(force=True, silent=True) or {}
    password = data.get("password", "") or data.get("owner_password", "")
    if password == OWNER_PASSWORD:
        return jsonify({"ok": True, "message": "Welcome Boss, Owner Mode ON", "owner": "Abdulmalik Muazu Abba", "contact": OWNER_PHONE})
    return jsonify({"ok": False, "message": "Wrong password - Owner only"}), 403

# ===== UPLOAD - IMAGE / VOICE / CLIP - USER CAN SEND BUT CANNOT CHANGE ANYTHING =====
@app.route("/gai-upload", methods=["POST"])
def gai_upload():
    try:
        # Works with form-data file or JSON base64
        if "file" in request.files:
            f = request.files["file"]
            filename = f.filename or "upload"
            # Save to uploads folder
            os.makedirs("uploads", exist_ok=True)
            path = os.path.join("uploads", filename)
            f.save(path)
            return jsonify({"ok": True, "message": f"Received {filename}. GAIOS will read image / voice / clip. No settings changed.", "file": filename, "watermark": WATERMARK})
        data = request.get_json(force=True, silent=True) or {}
        if data.get("file_name") or data.get("type"):
            return jsonify({"ok": True, "message": f"Received {data.get('type','file')} - {data.get('file_name','upload')}. GAIOS will read it. No settings changed.", "watermark": WATERMARK})
        return jsonify({"ok": True, "message": "Send image, voice or clip using file field.", "watermark": WATERMARK})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

@app.route('/gai-chat', methods=['POST'])
def gai_chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        msg = data.get('message', '') or data.get('msg', '')
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": MEMORY_TEXT}, {"role": "user", "content": msg}], "temperature": 0.7}
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        reply = r.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Boss, Groq wahala small - " + str(e)})

@app.route('/gai-status', methods=['GET'])
def gai_status():
    return jsonify({"status": "CHAT GAI I mdey ON", "owner": "Abdulmalik Muazu Abba", "model": "openai/gpt-oss-120b", "location": "Port Harcourt", "brand": "GAIOS", "version": "GAIOS V5.0", "auto_theme": get_auto_theme(), "contact": OWNER_PHONE})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = data.get("msg", "") or data.get("message", "")
    low = msg.lower()
    if "who be me" in low or "who am i" in low or "wetin you know about me" in low or "my name" in low:
        return jsonify({"reply": f"Na you be my Boss 👑 <br><br><b>Name:</b> Abdulmalik Muazu Abba<br><b>Nationality:</b> Nigeria<br><b>Origin:</b> Kano State<br><br>You build me - CHAT GAI / GAIOS - with Pydroid + Groq for Android. You no dey give up, you fight code wahala till e work. Na your legacy be this. I go remember you forever."})
    try:
        r = requests.post(GROQ_URL, headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "application/json"}, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": MEMORY_TEXT}, {"role": "user", "content": msg}], "temperature": 0.7, "max_tokens": 600}, timeout=20)
        d = r.json()
        txt = d["choices"][0]["message"]["content"]
        return jsonify({"reply": txt})
    except Exception as e:
        return jsonify({"reply": "Groq error: " + str(e)})

@app.route("/gai-owner", methods=["POST"])
def gai_owner():
    data = request.get_json(force=True, silent=True) or {}
    if not is_owner(data):
        return jsonify({"error": "Owner Mode only. Only Abdulmalik can access."}), 403
    action = data.get("action", "")
    settings = load_json("gaios_settings.json", {"theme": "default", "auto_theme": True, "language": "Pidgin + English"})
    if action == "change_theme":
        theme = data.get("theme", "default")
        if theme in THEMES:
            settings["theme"] = theme
            save_json("gaios_settings.json", settings)
            return jsonify({"ok": True, "theme": THEMES[theme], "message": f"Theme changed to {THEMES[theme]['name']}"})
        return jsonify({"error": "Theme not found", "themes": list(THEMES.keys())})
    if action == "add_feature":
        feats = load_json("gaios_features.json", [])
        feats.append({"feature": data.get("feature"), "added_at": datetime.now().isoformat()})
        save_json("gaios_features.json", feats)
        return jsonify({"ok": True, "message": "Feature added by Owner", "features": feats})
    if action == "toggle_auto_theme":
        settings["auto_theme"] = data.get("value", True)
        save_json("gaios_settings.json", settings)
        return jsonify({"ok": True, "auto_theme": settings["auto_theme"]})
    if action == "set_language":
        settings["language"] = data.get("language", "Pidgin + English")
        save_json("gaios_settings.json", settings)
        return jsonify({"ok": True, "language": settings["language"]})
    return jsonify({"ok": True, "settings": settings, "themes": THEMES})

@app.route("/gai-themes", methods=["GET"])
def gai_themes():
    settings = load_json("gaios_settings.json", {"theme": "default", "auto_theme": True})
    current = settings["theme"]
    if settings.get("auto_theme"):
        current = get_auto_theme()
    return jsonify({"themes": THEMES, "current_theme": current, "auto_theme": settings.get("auto_theme", True), "current_details": THEMES.get(current)})

@app.route("/gai-business", methods=["GET", "POST"])
def gai_business():
    if request.method == "GET":
        sales = load_json("sales.json", [])
        tasks = load_json("tasks.json", [])
        customers = load_json("customers.json", [])
        total = sum([s.get("amount", 0) for s in sales])
        return jsonify({"goals": {"A": "Sell 50 sticker packs/week", "B": "Get 10 App Builder customers", "C": "Open Drawing + Book Store"}, "total_sales": total, "sales_count": len(sales), "sales": sales, "tasks": tasks, "customers": customers, "contact": OWNER_PHONE})
    data = request.get_json(force=True, silent=True) or {}
    typ = data.get("type", "sale")
    if typ == "sale":
        sales = load_json("sales.json", [])
        sales.append({"product": data.get("product"), "amount": data.get("amount", 0), "customer": data.get("customer"), "date": datetime.now().isoformat(), "paid": data.get("paid", True)})
        save_json("sales.json", sales)
        return jsonify({"ok": True, "sales": sales})
    if typ == "task":
        tasks = load_json("tasks.json", [])
        tasks.append({"task": data.get("task"), "done": False, "date": datetime.now().isoformat()})
        save_json("tasks.json", tasks)
        return jsonify({"ok": True, "tasks": tasks})
    if typ == "customer":
        customers = load_json("customers.json", [])
        customers.append({"name": data.get("name"), "phone": data.get("phone"), "bought": data.get("bought"), "date": datetime.now().isoformat()})
        save_json("customers.json", customers)
        return jsonify({"ok": True, "customers": customers})
    return jsonify({"error": "type must be sale/task/customer"})

@app.route("/gai-shop", methods=["GET", "POST"])
def gai_shop():
    if request.method == "GET":
        shop = load_json("shop.json", {"drawings": [], "books": []})
        return jsonify(shop)
    data = request.get_json(force=True, silent=True) or {}
    if not is_owner(data):
        if data.get("type") == "order":
            orders = load_json("orders.json", [])
            orders.append({"product": data.get("product"), "customer": data.get("customer"), "phone": data.get("phone"), "date": datetime.now().isoformat()})
            save_json("orders.json", orders)
            return jsonify({"ok": True, "message": f"Order received. Contact {OWNER_PHONE} - Text Only", "orders": orders})
        return jsonify({"error": "Only Owner can add products"}), 403
    shop = load_json("shop.json", {"drawings": [], "books": []})
    cat = data.get("category", "drawings")
    if cat not in shop:
        shop[cat] = []
    shop[cat].append({"title": data.get("title"), "price": data.get("price"), "image": data.get("image", ""), "desc": data.get("desc", ""), "watermark": WATERMARK})
    save_json("shop.json", shop)
    return jsonify({"ok": True, "shop": shop})

@app.route("/gai-stickers", methods=["GET", "POST"])
def gai_stickers():
    if request.method == "GET":
        return jsonify({"categories": STICKER_CATEGORIES, "styles": ["Premium", "Cute"], "watermark": WATERMARK, "contact": OWNER_PHONE})
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({"ok": True, "message": "Sticker request saved. GAIOS will create with watermark.", "category": data.get("category"), "style": data.get("style", "Premium"), "text": data.get("text"), "watermark": WATERMARK})

@app.route("/gai-notes", methods=["GET", "POST"])
def gai_notes():
    if request.method == "GET":
        return jsonify({"notes": load_json("notes.json", [])})
    data = request.get_json(force=True, silent=True) or {}
    notes = load_json("notes.json", [])
    notes.append({"note": data.get("note"), "date": datetime.now().isoformat()})
    save_json("notes.json", notes)
    try:
        mem = open("memory.json").read() if os.path.exists("memory.json") else ""
        open("memory.json", "w").write(mem + f"\nNote {datetime.now().isoformat()}: {data.get('note')}")
    except:
        pass
    return jsonify({"ok": True, "notes": notes})

@app.route("/gai-status-creator", methods=["POST"])
def gai_status_creator():
    data = request.get_json(force=True, silent=True) or {}
    topic = data.get("topic", "GAIOS")
    try:
        r = requests.post(GROQ_URL, headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "application/json"}, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": "You write WhatsApp status, captions, posters in pure English, in Abdulmalik style. Always add: Questions? Text Only, No Calls - +234 812 152 1859. Made by GAIOS"}, {"role": "user", "content": f"Write WhatsApp status for: {topic}"}], "temperature": 0.7, "max_tokens": 300}, timeout=20)
        txt = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": txt})
    except Exception as e:
        return jsonify({"reply": "Groq error: " + str(e)})

if __name__ == "__main__":
    print("CHAT GAI / GAIOS V5.0 Loaded for Abdulmalik Muazu Abba")
    print("Features: Business Partner, Shop, Themes, Stickers, Owner Mode, Upload")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
