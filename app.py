from flask import Flask, render_template, request, redirect, session, jsonify, render_template_string
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = "bossmuddy-final-2026"

JINA_KUPOKEA = "TUHUMA MUHAMMED ALLY"
ADMIN_CRED = {"user": "boss", "pass": "1234"} # Hii ndio utabadilisha
PASSWORD_YA_SIKU = {"password": "BOSS15"}
wateja = []

LOGIN_HTML = """<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 text-white flex items-center justify-center min-h-screen p-4"><form method="POST" class="bg-slate-800 p-6 rounded-2xl w-full max-w-sm">
<h1 class="text-xl font-bold text-center">BOSS MUDDY - MFUMO</h1>{% if error %}<div class="bg-red-600 p-2 rounded mt-3 text-sm">{{error}}</div>{% endif %}
<input name="user" placeholder="Username" class="w-full p-3 text-black rounded mt-4" required><input name="pass" type="password" placeholder="Password" class="w-full p-3 text-black rounded mt-3" required>
<button class="bg-green-600 w-full p-3 rounded-xl mt-4 font-bold">INGIA NDANI</button></form></body></html>"""

ADMIN_HTML = """
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 text-white p-4">
<div class="flex justify-between"><h1 class="font-bold">BOSS DASHBOARD</h1><a href="/admin/logout" class="bg-red-600 px-3 py-1 rounded text-xs">Toka</a></div>
<div class="grid grid-cols-2 gap-2 mt-3"><div class="bg-green-700 p-3 rounded-xl"><p class="text-[10px]">HELA LEO</p><p class="font-bold">{{hela_leo}} TZS</p></div><div class="bg-blue-700 p-3 rounded-xl"><p class="text-[10px]">JUMLA</p><p class="font-bold">{{hela_mwezi}} TZS</p></div></div>

<div class="bg-yellow-400 text-black p-3 rounded-xl mt-4"><p class="font-black text-sm">🔑 PASSWORD YA LEO (Wote watapewa hii)</p>
<form action="/admin/set-daily-pass" method="POST" class="flex gap-2 mt-2"><input name="daily_password" value="{{password_leo}}" class="p-2 rounded flex-1 font-bold text-black" required><button class="bg-black text-white px-4 rounded font-bold">WEKA</button></form></div>

<div class="bg-white text-black p-3 rounded-xl mt-4"><p class="font-black">🔐 BADILISHA LOGIN YAKO YA KUINGILIA</p>
<form action="/admin/change-login" method="POST" class="grid gap-2 mt-2">
<input name="new_user" value="{{admin_user}}" placeholder="Username mpya" class="p-2 border rounded" required>
<input name="new_pass" placeholder="Password mpya" class="p-2 border rounded" required>
<button class="bg-black text-white p-2 rounded font-bold">BADILISHA LOGIN</button></form>
<p class="text-[10px] mt-1">Sasa: {{admin_user}} / {{admin_pass}}</p></div>

<div class="bg-white text-black p-3 rounded-xl mt-4"><p class="font-black">➕ ADD MANUAL</p><form action="/admin/add" method="POST" class="grid gap-2 mt-2"><input name="jina" placeholder="Jina" required class="p-2 border rounded"><input name="simu" placeholder="Simu" required class="p-2 border rounded"><select name="aina" class="p-2 border rounded"><option value="siku">Siku - 1000</option><option value="mwezi">Mwezi - 10000</option></select><button class="bg-black text-white p-2 rounded font-bold">MUUNGE</button></form></div>

<div class="mt-5"><h2 class="font-bold">WATEJA - MUDA UNAHESABU (24H)</h2>
{% for m in wateja %}
<div class="bg-slate-800 p-3 rounded-xl mt-2">
<div class="flex justify-between"><b>{{m.jina}}</b><span class="bg-yellow-400 text-black px-2 rounded text-xs font-bold">{{m.password}}</span></div>
<div class="text-[11px] text-slate-300 mt-1">Simu: {{m.simu}} | Lipia: {{m.lipwa}} TZS</div>
<div class="text-[11px]">Login: {{m.siku_str}} </div>
<div class="mt-1 text-xs">Muda uliobaki: <span class="countdown font-bold text-green-400" data-mwisho="{{m.mwisho}}">Loading...</span></div>
<div class="w-full bg-slate-700 h-2 rounded mt-1"><div class="h-2 bg-green-500 rounded progress-bar" data-mwisho="{{m.mwisho}}"></div></div>
</div>
{% endfor %}
</div>

<script>
function updateTimers(){
 document.querySelectorAll('.countdown').forEach(el=>{
  const mwisho = new Date(el.dataset.mwisho);
  const sasa = new Date();
  const diff = mwisho - sasa;
  if(diff<=0){ el.innerText='MUDA UMEISHA ❌'; el.classList.add('text-red-500'); return; }
  const h=Math.floor(diff/3600000); const m=Math.floor((diff%3600000)/60000); const s=Math.floor((diff%60000)/1000);
  el.innerText=`${h}h ${m}m ${s}s`;
 });
 document.querySelectorAll('.progress-bar').forEach(el=>{
  const mwisho=new Date(el.dataset.mwisho); const mwanzo=new Date(el.dataset.mwisho); mwanzo.setDate(mwanzo.getDate()-1);
  const total=24*3600*1000; const baki=mwisho-new Date(); const percent=Math.max(0, (baki/total)*100);
  el.style.width=percent+'%'; if(percent<20) el.classList.add('bg-red-500');
 });
}
setInterval(updateTimers,1000); updateTimers();
</script>
</body></html>
"""

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/lipa-push', methods=['POST'])
def lipa_push():
    data=request.json; phone=data.get('phone'); amount=int(data.get('amount',1000)); jina=data.get('jina',f"Mteja {phone}")
    password=PASSWORD_YA_SIKU["password"]; mwisho=datetime.now()+timedelta(days=1 if amount==1000 else 15)
    wateja.append({"id":len(wateja)+1,"jina":jina,"simu":phone,"aina":"siku" if amount==1000 else "mwezi","lipwa":amount,"password":password,"mwisho":mwisho.isoformat(),"siku":datetime.now(),"siku_str":datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    return jsonify({"success":True,"password":password})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('user')==ADMIN_CRED["user"] and request.form.get('pass')==ADMIN_CRED["pass"]:
            session['admin']=True; return redirect('/admin')
        return render_template_string(LOGIN_HTML, error="Login sio sahihi!")
    return render_template_string(LOGIN_HTML)

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect('/admin/login')
    leo=datetime.now().date(); wateja_leo=[m for m in wateja if m['siku'].date()==leo] if wateja else []
    hela_leo=sum([m.get('lipwa',0) for m in wateja_leo]); hela_mwezi=sum([m.get('lipwa',0) for m in wateja])
    return render_template_string(ADMIN_HTML, wateja=list(reversed(wateja)), wateja_leo=wateja_leo, hela_leo=hela_leo, hela_mwezi=hela_mwezi, password_leo=PASSWORD_YA_SIKU["password"], admin_user=ADMIN_CRED["user"], admin_pass=ADMIN_CRED["pass"])

@app.route('/admin/set-daily-pass', methods=['POST'])
def set_daily():
    if not session.get('admin'): return redirect('/admin/login')
    PASSWORD_YA_SIKU["password"]=request.form.get('daily_password'); return redirect('/admin')

@app.route('/admin/change-login', methods=['POST'])
def change_login():
    if not session.get('admin'): return redirect('/admin/login')
    ADMIN_CRED["user"]=request.form.get('new_user'); ADMIN_CRED["pass"]=request.form.get('new_pass'); return redirect('/admin')

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('admin'): return redirect('/admin/login')
    jina=request.form.get('jina'); simu=request.form.get('simu'); aina=request.form.get('aina')
    mwisho=datetime.now()+timedelta(days=1 if aina=='siku' else 15)
    wateja.append({"id":len(wateja)+1,"jina":jina,"simu":simu,"aina":aina,"lipwa":1000 if aina=='siku' else 10000,"password":PASSWORD_YA_SIKU["password"],"mwisho":mwisho.isoformat(),"siku":datetime.now(),"siku_str":datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    return redirect('/admin')

@app.route('/admin/logout')
def logout(): session.pop('admin', None); return redirect('/admin/login')
