import bcrypt
import string
import random
import os

from web import app
from flask import render_template, session, redirect, url_for, request
from werkzeug.utils import secure_filename


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
    if session.get('uid') is None:
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')


@app.route('/admin/products')
def products():
    if session.get('uid') is None:
        return redirect(url_for('login'))
    values = {}
    cursor = app.config['db'].cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    values.update({
        'products': products
    })
    return render_template('admin/products.html', values=values)


@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if session.get('uid') is None:
        return redirect(url_for('login'))
    values = {}
    if request.method == 'POST':
        missing = []
        form_data = request.form
        image = request.files['product_image']
        if not form_data.get('name') or form_data.get('name') == '':
            missing.append('Product Name')
        if not form_data.get('price') or form_data.get('price') == '':
            missing.append('Product Price')
        if not form_data.get('description') or form_data.get('description') == '':
            missing.append('Product Description')
        if not image:
            missing.append('Product Image')
        if not missing:
            try:
                file_mime = secure_filename(image.filename.split('.')[1])
                file_new_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(15)) + '.'+file_mime
                image.save(os.path.join(app.config['UPLOAD_PATH'], file_new_name))
                cursor = app.config['db'].cursor()
                query = "INSERT INTO Image(name) VALUES (\"%s\")" % (file_new_name)
                cursor.execute(query)
                cursor.close()
                app.config['db'].commit()
                cursor = app.config['db'].cursor()
                cursor.execute("SELECT LAST_INSERT_ID();")
                image_id = cursor.fetchone()
                cursor.close()
                cursor = app.config['db'].cursor()
                query = "INSERT INTO Product (name, price, description, image_id) VALUES (\"%s\", %s, \"%s\", %s)" % (form_data.get('name'), form_data.get('price'), form_data.get('description'), image_id[0])
                cursor.execute(query)
                app.config['db'].commit()
                return redirect(url_for('products'))
            except Exception as e:
                print(e)
                values.update({'error': e})
    return render_template('admin/add_product.html')
