from web import app
from flask import render_template, session, redirect, url_for


@app.route('/login')
def login():
    return render_template('admin/templates/login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('uid') is None:
        return 'hello from dashboard'
    else:
        return redirect(url_for('login'))
