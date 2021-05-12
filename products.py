from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Products

@app.route('/products')
def products():
    table = Products.query.order_by(Products.id_product).all()
    return render_template("products.html", table=table)

@app.route('/products/create', methods=['POST', 'GET'])
def create_product():
    if request.method == "POST":
        name_product = request.form['name_product']
        type_product = request.form['type_product']
        amount_product = request.form['amount_product']
        id_shop = request.form['id_shop']
        price_product = request.form['price_product']

        products = Products(name_product=name_product, type_product=type_product, amount_product=amount_product,
                           id_shop=id_shop, price_product=price_product)

        db.session.add(products)
        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "Ошибочка"
    else:
        return render_template("products_create.html")