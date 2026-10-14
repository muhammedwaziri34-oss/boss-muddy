from flask import Flask, render_template, request, redirect
import os
app = Flask(__name__)
FILE = "wateja.txt"
@app.route("/")
def home():
    w = []
    if os.path.exists(FILE):
        for line in open(FILE):
            if "," in line:
                jina, simu = line.strip().split(",",1)
                w.append({"jina":jina,"simu":simu})
    return render_template("index.html", wateja=w)
@app.route("/sajili", methods=["POST"])
def sajili():
    jina = request.form.get("jina")
    simu = request.form.get("simu")
    if jina and simu:
        open(FILE,"a").write(f"{jina},{simu}\n")
    return redirect("/")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
