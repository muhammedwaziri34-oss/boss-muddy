from flask import Flask, render_template, request, jsonify
import random
import string
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# ===== NAMBA ZAKO NA JINA =====
JINA_KUPOKEA = "TUHUMA MUHAMMED ALLY"
MITANDAO = {
    "tigo": "0707037351",
    "vodacom": "0797740362",
    "halotel": "0611248500"
}

# Hifadhi password zilizotengenezwa
wifi_passwords = {}

def tengeneza_password():
    # Tengeneza password rahisi kama BM-4829
    return f"BM-{random.randint(1000,9999)}"

@app.route('/')
def index():
    return render_template('index.html', jina=JINA_KUPOKEA, mitandao=MITANDAO)

@app.route('/api/lipa-push', methods=['POST'])
def lipa_push():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')
    network = data.get('network', 'tigo')

    if not phone:
        return jsonify({"success": False, "message": "Weka namba"}), 400

    # HAPA NDIPO PUSH INATUMWA - Kwa sasa tunasimulate
    # Baadaye tuta-connect na Selcom / Tigo API

    # Tengeneza password mara moja
    password = tengeneza_password()
    expire = datetime.now() + timedelta(days=1 if int(amount)==1000 else 7 if int(amount)==5000 else 30)

    wifi_passwords[phone] = {
        "password": password,
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expire": expire.strftime("%Y-%m-%d"),
        "phone": phone
    }

    print(f"MTEJA ALIYELIPA: {phone} -> PASSWORD: {password}")

    return jsonify({
        "success": True,
        "message": "Malipo yamepokelewa!",
        "password": password,
        "wifi_name": "BossMuddy-WIFI",
        "expire": wifi_passwords[phone]['expire'],
        "jina": JINA_KUPOKEA,
        "kulipia": MITANDAO[network]
    })

@app.route('/api/admin/passwords')
def admin_passwords():
    return jsonify(wifi_passwords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
@app.route('/api/lipa-push', methods=['POST'])
def lipa_push():
    import random
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount', 1000)

    password = f"BM-{random.randint(1000,9999)}"

    # Tafuta mteja na muwekee password
    for m in wateja:
        if m['simu'] == phone:
            m['password'] = password

    return jsonify({
        "success": True,
        "password": password,
        "wifi_name": "BossMuddy-WIFI"
    })
