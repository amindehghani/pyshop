import bcrypt

from web import app
from flask import render_template, session, redirect, url_for, request


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('uid'):
        return redirect(url_for('dashboard'))
    values = {}
    if request.method == 'POST':
        missing = []
        form_data = request.form
        if not form_data.get('email') or form_data.get('email') == '':
            missing.append('email')
        if not form_data.get('password') or form_data.get('password') == '':
            missing.append('password')
        if not missing:
            try:
                db = app.config['db']
                cursor = db.cursor()
                cursor.execute("SELECT id, password FROM User WHERE email=\"%s\"" % form_data.get('email'))
                user = cursor.fetchone()
                if user:
                    passwd = user[1]
                    if bcrypt.checkpw(form_data.get('password').encode('utf-8'), passwd.encode('utf-8')):
                        session['uid'] = user[0]
                        return redirect(url_for('dashboard'))
                    else:
                        values.update({'error': 'Password is incorrect'})
                else:
                    values.update({'error': 'User not found'})
            except Exception as e:
                print(e)
                values.update({'error': e})
        if missing:
            values.update({'missing': missing})
    return render_template('login.html', values=values)


@app.route('/admin/dashboard')
def dashboard():
    if not session.get('uid') is None:
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/admin/products')
def products():
    if not session.get('uid') is None:
        return render_template('admin/products.html')
    else:
        return redirect(url_for('login'))
