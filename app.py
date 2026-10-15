@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('admin'): return redirect('/admin/login')
    jina = request.form.get('jina')
    simu = request.form.get('simu')
    aina = request.form.get('aina')
    password_custom = request.form.get('password')
    import random
    from datetime import datetime, timedelta
    password = password_custom if password_custom else f"BM-{random.randint(1000,9999)}"
    mwisho = datetime.now() + timedelta(days=1 if aina=='siku' else 15)
    wateja.append({"id": len(wateja)+1, "jina": jina, "simu": simu, "aina": aina, "lipwa": 1000 if aina=='siku' else 10000, "password": password, "mwisho": mwisho.isoformat(), "siku": datetime.now().isoformat()})
    save_wateja()
    return redirect('/admin')
