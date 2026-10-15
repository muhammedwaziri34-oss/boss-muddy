from flask import Flask, render_template, request, redirect, session, jsonify, render_template_string
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "bossmuddy-2025-tuhuma-ally-final"

JINA_KUPOKEA = "TUHUMA MUHAMMED ALLY"
MITANDAO = {"tigo": "0707037351", "vodacom": "0797740362", "halotel": "0611248500"}

ADMIN_USER = "boss"
ADMIN_PASS = "1234"

# HAPA NDIPO WEWE UNAWEKA PASSWORD YA SIKU - INABADILIKA KILA SIKU
PASSWORD_YA_SIKU = {"password": "BOSS15", "date": "2025-01"} # Default

wateja = []

# ===== TEMPLATE ZA ADMIN NDANI YA APP.PY (Ili isilete Internal Error) =====
LOGIN_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 text-white flex items-center justify-center min-h-screen p-4">
<form method="POST" class="bg-slate-800 p-6 rounded-2xl w-full max-w-sm">
<h1 class="text-2xl font-bold text-center">BOSS MUDDY ADMIN</h1>
<p class="text-center text-xs text-slate-400">TUHUMA MUHAMMED ALLY</p>
{% if error %}<div class="bg-red-600 p-2 rounded mt-4 text-sm">{{error}}</div>{% endif %}
<input name="user" placeholder="boss" value="boss" class="w-full p-3 text-black rounded mt-4" required>
<input name="pass" type="password" placeholder="1234" class="w-full p-3 text-black rounded mt-3" required>
<button class="bg-green-600 w-full p-3 rounded-xl mt-4 font-bold">INGIA</button>
</form></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 text-white p-4">
<div class="flex justify-between"><h1 class="text-xl font-bold">ADMIN DASHBOARD</h1><a href="/admin/logout" class="bg-red-600 px-3 py-1 rounded text-sm">Toka</a></div>

<div class="grid grid-cols-2 gap-3 mt-4">
<div class="bg-green-700 p-4 rounded-xl"><p class="text-xs">HELA LEO</p><p class="text-2xl font-bold">{{hela_leo}} TZS</p><p class="text-xs">{{wateja_leo|length}} watu</p></div>
<div class="bg-blue-700 p-4 rounded-xl"><p class="text-xs">JUMLA</p><p class="text-2xl font-bold">{{hela_mwezi}} TZS</p><p class="text-xs">{{wateja|length}} wote</p></div>
</div>

<div class="bg-yellow-500 text-black p-4 rounded-2xl mt-5">
<h2 class="font-black text-lg">🔑 WEKA PASSWORD YA LEO HAPA</h2>
<p class="text-xs">Password unayoweka hapa ndiyo kila mteja akilipa ataiona!</p>
<form action="/admin/set-daily-pass" method="POST" class="flex gap-2 mt-3">
<input name="daily_password" value="{{password_leo}}" placeholder="mfano BOSS15" required class="p-3 border-2 rounded-xl flex-1 text-black font-bold">
<button class="bg-black text-white px-6 rounded-xl font-bold">WEKA</button>
</form>
<p class="mt-2 text-sm font-bold">Sasa Password ya Leo ni: <span class="text-2xl">{{password_leo}}</span></p>
</div>

<div class="bg-white text-black p-4 rounded-2xl mt-5">
<h2 class="font-black">➕ ADD MTU MANUAL</h2>
<form action="/admin/add" method="POST" class="grid gap-2 mt-2">
<input name="jina" placeholder="Jina" required class="p-2 border rounded">
<input name="simu" placeholder="Simu 07..." required class="p-2 border rounded">
<select name="aina" class="p-2 border rounded"><option value="siku">Siku - 1000</option><option value="mwezi">Mwezi - 10000</option></select>
<button class="bg-black text-white p-2 rounded font-bold">MUUNGE</button>
</form>
</div>

<div class="mt-6"><h2 class="font-bold">WATEJA ({{wateja|length}})</h2>
{% for m in wateja %}
<div class="bg-slate-800 p-3 rounded mt-2 text-sm"><b>{{m.jina}}</b> - {{m.simu}} - {{m.lipwa}} TZS<br>Password aliyopewa: {{m.password}}</div>
{% endfor %}
</div>
</body></html>
"""

@app.route('/')
def index():
    for m in wateja:
        try:
            mwisho = datetime.fromisoformat(m.get('mwisho',''))
            baki = mwisho - datetime.now()
            m['baki'] = str(baki).split('.')[0]
            m['status'] = 'MEKUNDU' if baki.total_seconds() < 0 else 'KIJANI'
        except:
            m['baki']='Active'; m['status']='KIJANI'
    return render_template('index.html', wateja=wateja, jina=JINA_KUPOKEA, mitandao=MITANDAO)

@app.route('/sajili', methods=['POST'])
def sajili():
    jina = request.form.get('jina'); simu = request.form.get('simu'); aina = request.form.get('aina')
    mwisho = datetime.now() + timedelta(days=1 if aina=='siku' else 15)
    wateja.append({"id": len(wateja)+1, "jina": jina, "simu": simu, "aina": aina, "lipwa": 1000 if aina=='siku' else 10000, "password": PASSWORD_YA_SIKU["password"], "mwisho": mwisho.isoformat(), "siku": datetime.now().isoformat()})
    return redirect('/')

@app.route('/lipia/<int:id>', methods=['POST'])
def lipia(id):
    for m in wateja:
        if m['id']==id:
            m['mwisho']=(datetime.now()+timedelta(days=1 if m['aina']=='siku' else 15)).isoformat()
            m['password']=PASSWORD_YA_SIKU["password"]
    return redirect('/')

@app.route('/api/lipa-push', methods=['POST'])
def lipa_push():
    data = request.json
    phone = data.get('phone')
    amount = int(data.get('amount', 1000))
    password = PASSWORD_YA_SIKU["password"]
    mwisho = datetime.now() + timedelta(days=1 if amount==1000 else 15)
    found=False
    for m in wateja:
        if m['simu']==phone:
            m['password']=password; m['mwisho']=mwisho.isoformat(); m['lipwa']=amount; found=True
    if not found:
        wateja.append({"id": len(wateja)+1, "jina": f"Mteja {phone}", "simu": phone, "aina": "siku" if amount==1000 else "mwezi", "lipwa": amount, "password": password, "mwisho": mwisho.isoformat(), "siku": datetime.now().isoformat()})
    return jsonify({"success": True, "password": password, "wifi_name": "BossMuddy-WIFI"})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('user')==ADMIN_USER and request.form.get('pass')==ADMIN_PASS:
            session['admin']=True
            return redirect('/admin')
        else:
            return render_template_string(LOGIN_HTML, error="Password si sahihi!")
    return render_template_string(LOGIN_HTML)

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect('/admin/login')
    leo = datetime.now().date()
    wateja_leo = [m for m in wateja if m.get('siku','')[:10]==str(leo)]
    hela_leo = sum([m.get('lipwa',0) for m in wateja_leo])
    hela_mwezi = sum([m.get('lipwa',0) for m in wateja])
    return render_template_string(ADMIN_HTML, wateja=wateja, wateja_leo=wateja_leo, hela_leo=hela_leo, hela_mwezi=hela_mwezi, password_leo=PASSWORD_YA_SIKU["password"], jina=JINA_KUPOKEA, mitandao=MITANDAO)

@app.route('/admin/set-daily-pass', methods=['POST'])
def set_daily():
    if not session.get('admin'): return redirect('/admin/login')
    new_pass = request.form.get('daily_password')
    PASSWORD_YA_SIKU["password"]=new_pass
    PASSWORD_YA_SIKU["date"]=str(datetime.now().date())
    return redirect('/admin')

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('admin'): return redirect('/admin/login')
    jina = request.form.get('jina'); simu = request.form.get('simu'); aina = request.form.get('aina')
    mwisho = datetime.now() + timedelta(days=1 if aina=='siku' else 15)
    wateja.append({"id": len(wateja)+1, "jina": jina, "simu": simu, "aina": aina, "lipwa": 1000 if aina=='siku' else 10000, "password": PASSWORD_YA_SIKU["password"], "mwisho": mwisho.isoformat(), "siku": datetime.now().isoformat()})
    return redirect('/admin')

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin/login')
