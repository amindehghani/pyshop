from web import app
from flask import render_template, send_from_directory, abort


@app.route('/')
def index():
    values = {}
    cursor = app.config['db'].cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    values.update({
        'products': products
    })
    return render_template('public/shop.html', values=values)


@app.route('/product/<id>')
def product(id):
    cursor = app.config['db'].cursor()
    cursor.execute('SELECT * FROM Product WHERE id=%s' % int(id))
    product = cursor.fetchone()
    if product:
        return render_template('public/product.html', product=product)
    abort(404)

@app.route('/uploads/<id>')
def send_file(id):
    cursor = app.config['db'].cursor()
    cursor.execute("SELECT name FROM Image WHERE id=%s" % int(id))
    image_name = cursor.fetchone()
    return send_from_directory(app.config['UPLOAD_PATH'], image_name[0])


@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404
