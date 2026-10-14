from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Chukua DATABASE_URL kutoka Vercel/Neon
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
FILE = "wateja.txt"

def get_wateja():
    w = []
    if DATABASE_URL:
        try:
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            # Tengeneza table kama haipo
            cur.execute("CREATE TABLE IF NOT EXISTS wateja (id SERIAL PRIMARY KEY, jina TEXT, simu TEXT);")
            conn.commit()
            cur.execute("SELECT jina, simu FROM wateja ORDER BY id DESC;")
            for jina, simu in cur.fetchall():
                w.append({"jina": jina, "simu": simu})
            cur.close()
            conn.close()
            return w
        except Exception as e:
            print(f"DB Error: {e}")

    # Fallback ya local (wateja.txt)
    if os.path.exists(FILE):
        for line in open(FILE, encoding="utf-8"):
            if "," in line:
                jina, simu = line.strip().split(",",1)
                w.append({"jina":jina,"simu":simu})
    return w

def save_mteja(jina, simu):
    if DATABASE_URL:
        try:
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS wateja (id SERIAL PRIMARY KEY, jina TEXT, simu TEXT);")
            cur.execute("INSERT INTO wateja (jina, simu) VALUES (%s, %s);", (jina, simu))
            conn.commit()
            cur.close()
            conn.close()
            return
        except Exception as e:
            print(f"DB Error: {e}")

    open(FILE,"a", encoding="utf-8").write(f"{jina},{simu}\n")

@app.route("/")
def home():
    wateja = get_wateja()
    return render_template("index.html", wateja=wateja)

@app.route("/sajili", methods=["POST"])
def sajili():
    jina = request.form.get("jina")
    simu = request.form.get("simu")
    if jina and simu:
        save_mteja(jina, simu)
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)