from flask import Flask, render_template, request, redirect, session, jsonify
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "bossmuddy-2025-tuhuma-ally"

# JINA LAKO
JINA_KUPOKEA = "TUHUMA MUHAMMED ALLY"
MITANDAO = {
    "tigo": "0707037351",
    "vodacom": "0797740362",
    "halotel": "0611248500"
}

# ADMIN
ADMIN_USER = "boss"
ADMIN_PASS = "1234"

# HIFADHI KWA MEMORY TU (Vercel hairuhusu file)
wateja = []

def tengeneza_password():
    return f"BM-{random.randint(1000,9999)}"

@app.route('/')
def index():
    for m in wateja:
        try:
            mwisho = datetime.fromisoformat(m.get('mwisho',''))
            baki = mwisho - datetime.now()
            m['baki'] = str(baki).split('.')[0]
            m['status'] = 'MEKUNDU' if baki.total_seconds() < 0 else 'NJANO' if baki.total_seconds() < 3600 else 'KIJANI'
        except:
            m['baki'] = 'Active'
            m['status'] = 'KIJANI'
    return render_template('index.html', wateja=wateja, jina=JINA_KUPOKEA, mitandao=MITANDAO)

@app.route('/sajili', methods=['POST'])
def sajili():
    jina = request.form.get('jina')
    simu = request.form.get('simu')
    aina = request.form.get('aina')
    days = 1 if aina=='siku' else 15
    amount = 1000 if aina=='siku' else 10000
    password = tengeneza_password()
    mwisho = datetime.now() + timedelta(days=days)
    wateja.append({
        "id": len(wateja)+1,
        "jina": jina,
        "simu": simu,
        "aina": aina,
        "lipwa": amount,
        "password": password,
        "mwisho": mwisho.isoformat(),
        "siku": datetime.now().isoformat()
    })
    return redirect('/')

@app.route('/lipia/<int:id>', methods=['POST'])
def lipia(id):
    for m in wateja:
        if m['id']==id:
            days = 1 if m['aina']=='siku' else 15
            m['mwisho'] = (datetime.now() + timedelta(days=days)).isoformat()
            m['password'] = tengeneza_password()
    return redirect('/')

@app.route('/api/lipa-push', methods=['POST'])
def lipa_push():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount', 1000)
    password = tengeneza_password()
    mwisho = datetime.now() + timedelta(days=1 if int(amount)==1000 else 15)
    found=False
    for m in wateja:
        if m['simu']==phone:
            m['password']=password
            m['mwisho']=mwisho.isoformat()
            m['lipwa']=amount
            found=True
    if not found:
        wateja.append({
            "id": len(wateja)+1,
            "jina": f"Mteja {phone}",
            "simu": phone,
            "aina": "siku" if int(amount)==1000 else "mwezi",
            "lipwa": amount,
            "password": password,
            "mwisho": mwisho.isoformat(),
            "siku": datetime.now().isoformat()
        })
    return jsonify({"success": True, "password": password, "wifi_name": "BossMuddy-WIFI"})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('user')==ADMIN_USER and request.form.get('pass')==ADMIN_PASS:
            session['admin']=True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error="Password si sahihi!")
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect('/admin/login')
    leo = datetime.now().date()
    wateja_leo = [m for m in wateja if 'siku' in m and m['siku'][:10]==str(leo)]
    hela_leo = sum([m.get('lipwa',0) for m in wateja_leo])
    hela_mwezi = sum([m.get('lipwa',0) for m in wateja])
    password_leo = f"BOSS-{leo.strftime('%d%m')}"
    return render_template('admin.html', wateja=wateja, wateja_leo=wateja_leo, hela_leo=hela_leo, hela_mwezi=hela_mwezi, password_leo=password_leo, jina=JINA_KUPOKEA, mitandao=MITANDAO)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('admin'): return redirect('/admin/login')
    jina = request.form.get('jina')
    simu = request.form.get('simu')
    aina = request.form.get('aina')
    password_custom = request.form.get('password')
    password = password_custom if password_custom else tengeneza_password()
    mwisho = datetime.now() + timedelta(days=1 if aina=='siku' else 15)
    wateja.append({
        "id": len(wateja)+1,
        "jina": jina,
        "simu": simu,
        "aina": aina,
        "lipwa": 1000 if aina=='siku' else 10000,
        "password": password,
        "mwisho": mwisho.isoformat(),
        "siku": datetime.now().isoformat()
    })
    return redirect('/admin')

@app.route('/admin/set-password', methods=['POST'])
def set_password():
    if not session.get('admin'): return redirect('/admin/login')
    simu = request.form.get('simu')
    new_pass = request.form.get('new_password')
    for m in wateja:
        if m['simu']==simu:
            m['password']=new_pass
    return redirect('/admin')

@app.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete(id):
    if not session.get('admin'): return redirect('/admin/login')
    global wateja
    wateja = [m for m in wateja if m['id']!=id]
    return redirect('/admin')

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin/login')

# Muhimu kwa Vercel
# app = app
