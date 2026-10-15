# app.py - BOSS MUDDY FINAL
from flask import Flask, request, jsonify, render_template, session
import json, random, time
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "boss-muddy-secret-2024"

# Faili zetu
WHITELIST = "whitelist.json"
WATEJA = "wateja.json" # Hapa ndipo hesabu ya maokoto

# 1. BASE YA MTEJA - Hii ndio mteja anaiona
@app.route('/')
def mteja_base():
    # Hapa tunamkamata MAC na IP yake automatically
    mac = request.args.get('mac') or request.remote_addr
    return render_template('index.html', mac=mac)

# 2. MTU AKIJISAJILI
@app.route('/api/jisajili', methods=['POST'])
def jisajili():
    data = request.json
    jina = data.get('jina')
    namba = data.get('namba')
    mac = data.get('mac')

    # Tunamtengenezea password ya kipekee - Hii inazuia scanning
    password = str(random.randint(100000, 999999))
    
    # Tunamhifadhi kwenye file ya wateja
    mteja = {
        "jina": jina,
        "namba": namba,
        "mac": mac,
        "password": password,
        "muda": str(datetime.now()),
        "status": "hajalipa"
    }
    
    # Hifadhi kwenye wateja.json
    try:
        with open(WATEJA, 'r') as f: wateja = json.load(f)
    except: wateja = []
    wateja.append(mteja)
    with open(WATEJA, 'w') as f: json.dump(wateja, f, indent=2)
    
    # Hapa ndipo unaweka PUSH ya TigoPesa / M-Pesa
    # Kwa sasa tunarudisha "lipa" ili app iite Tigo Pesa API
    return jsonify({"status": "sajili_ok", "password": password, "lipia": f"{namba} - Tsh 1000"})

# 3. BAADA YA MALIPO - Hii ndio ina-connect automatically
@app.route('/api/thibitisha-malipo', methods=['POST'])
def thibitisha():
    data = request.json
    mac = data.get('mac')
    plan = data.get('plan', '1day')
    
    # 1. Add kwenye whitelist.json yako
    try:
        with open(WHITELIST, 'r') as f: wl = json.load(f)
    except: wl = []
    
    expire = datetime.now() + timedelta(days=1 if plan=='1day' else 7)
    
    wl.append({
        "mac": mac,
        "plan": plan,
        "expire": str(expire),
        "password": data.get('password')
    })
    with open(WHITELIST, 'w') as f: json.dump(wl, f, indent=2)
    
    # 2. Hapa ndipo tunamwambia ZLT W304VA PRO 192.168.1.1 amfugulie
    # os.system(f"iptables -I FORWARD -m mac --mac-source {mac} -j ACCEPT")
    
    return jsonify({"status": "connected", "message": "Mteja ameunganishwa, internet inafanya kazi"})

# 4. BASE YA ADMIN - Hii ni yako peke yako
@app.route('/admin')
def admin_login():
    return render_template('admin.html') # Hii inaona maokoto yote

@app.route('/api/admin/maokoto')
def maokoto():
    try:
        with open(WATEJA, 'r') as f: return jsonify(json.load(f))
    except: return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
