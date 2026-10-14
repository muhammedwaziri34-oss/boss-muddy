from flask import Flask, render_template, request, redirect
import os, psycopg2
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")
TZ = pytz.timezone('Africa/Dar_es_Salaam')

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL: return
    try:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS wateja (
            id SERIAL PRIMARY KEY,
            jina TEXT, simu TEXT, aina TEXT,
            tarehe_kuanza TIMESTAMP, tarehe_mwisho TIMESTAMP,
            kiasi_kililipwa INT, status TEXT
        );""")
        conn.commit(); cur.close(); conn.close()
    except Exception as e: print(e)

init_db()

@app.route("/")
def home():
    w=[]
    try:
        if DATABASE_URL:
            conn=get_conn(); cur=conn.cursor()
            cur.execute("SELECT id,jina,simu,aina,tarehe_kuanza,tarehe_mwisho,kiasi_kililipwa FROM wateja ORDER BY id DESC")
            rows=cur.fetchall()
            now=datetime.now(TZ)
            for id,jina,simu,aina,kuanza,mwisho,lipwa in rows:
                if mwisho:
                    mwisho = mwisho.astimezone(TZ) if mwisho.tzinfo else TZ.localize(mwisho)
                    diff = (mwisho - now).total_seconds()
                    if diff <=0: st="MEKUNDU"
                    elif diff < 7200: st="NJANO"
                    elif aina=='mwezi' and diff < 172800: st="NJANO"
                    else: st="KIJANI"
                    baki = f"{int(diff//3600)}h {int((diff%3600)//60)}m" if diff>0 else "IMEISHA"
                else:
                    st="KIJANI"; baki="-"
                w.append({"id":id,"jina":jina,"simu":simu,"aina":aina,"mwisho":mwisho,"lipwa":lipwa,"status":st,"baki":baki})
            cur.close(); conn.close()
    except Exception as e: print(e)
    return render_template("index.html",wateja=w)

@app.route("/sajili",methods=["POST"])
def sajili():
    jina=request.form.get("jina"); simu=request.form.get("simu"); aina=request.form.get("aina")
    now=datetime.now(TZ)
    mwisho = now+timedelta(hours=24) if aina=="siku" else now+timedelta(days=15)
    lipwa = 1000 if aina=="siku" else 10000
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO wateja (jina,simu,aina,tarehe_kuanza,tarehe_mwisho,kiasi_kililipwa,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(jina,simu,aina,now,mwisho,lipwa,"Active"))
    conn.commit(); cur.close(); conn.close()
    return redirect("/")

@app.route("/lipia/<int:id>",methods=["POST"])
def lipia(id):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("SELECT aina,tarehe_mwisho FROM wateja WHERE id=%s",(id,))
    row=cur.fetchone()
    if row:
        aina,mwisho=row; now=datetime.now(TZ)
        if aina=="mwezi":
            base = mwisho.astimezone(TZ) if mwisho and mwisho.tzinfo else (TZ.localize(mwisho) if mwisho else now)
            if base < now: base=now
            new_mwisho=base+timedelta(days=15)
            cur.execute("UPDATE wateja SET tarehe_mwisho=%s, kiasi_kililipwa=kiasi_kililipwa+10000 WHERE id=%s",(new_mwisho,id))
        else:
            new_mwisho=now+timedelta(hours=24)
            cur.execute("UPDATE wateja SET tarehe_kuanza=%s, tarehe_mwisho=%s, kiasi_kililipwa=1000 WHERE id=%s",(now,new_mwisho,id))
        conn.commit()
    cur.close(); conn.close()
    return redirect("/")
