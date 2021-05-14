from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Products


@app.route('/products')
def products():
    if "action" in request.args:
        if request.args["action"] == "del":  # для обратобки кнопки delete
            id_product = request.args['id']
            product = Products.query.get_or_404(id_product)

            try:
                db.session.delete(product)
                db.session.commit()
                return redirect("/products")
            except:
                return "При удалении записи произошла ошибка"
        elif request.args["action"] == "choice":
            id_product_lst = [request.args['id_product']]
            name_product_lst = [request.args['name_product']]
            type_product_lst = [request.args['type_product']]
            amount_product_lst = [request.args['amount_product']]
            id_shop_lst = [request.args['id_shop']]
            price_product_lst = [request.args['price_product']]

            if request.args['id_product'] == "any":
                temp = db.session.execute(f"SELECT id_product from Products").fetchall()
                id_product_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['name_product'] == "any":
                temp = db.session.execute(f"SELECT name_product from Products").fetchall()
                name_product_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['type_product'] == "any":
                temp = db.session.execute(f"SELECT type_product from Products").fetchall()
                type_product_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['amount_product'] == "any":
                temp = db.session.execute(f"SELECT amount_product from Products").fetchall()
                amount_product_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['id_shop'] == "any":
                temp = db.session.execute(f"SELECT id_shop from Products").fetchall()
                id_shop_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['price_product'] == "any":
                temp = db.session.execute(f"SELECT price_product from Products").fetchall()
                price_product_lst = [temp[i][0] for i in range(len(temp))]

            table = db.session.query(Products)\
                .filter(Products.id_product.in_(id_product_lst))\
                .filter(Products.name_product.in_(name_product_lst))\
                .filter(Products.type_product.in_(type_product_lst))\
                .filter(Products.amount_product.in_(amount_product_lst))\
                .filter(Products.id_shop.in_(id_shop_lst))\
                .filter(Products.price_product.in_(price_product_lst))
            return render_template("products.html", table=table)
        else:
            return redirect("/products")
    else:
        table = Products.query.order_by(Products.id_product).all()
        return render_template("products.html", table=table)


@app.route('/product-choice', methods=['POST'])
def product_choice():
    return redirect(f"/products?action=choice"
                    f"&id_product={request.form['id_product']}"
                    f"&name_product={request.form['name_product']}"
                    f"&type_product={request.form['type_product']}"
                    f"&amount_product={request.form['amount_product']}"
                    f"&id_shop={request.form['id_shop']}"
                    f"&price_product={request.form['price_product']}")


@app.route('/products/<int:id>/edit', methods=['POST', 'GET'])
def edit_product(id):
    product = Products.query.get_or_404(id)
    if request.method == "POST":
        product.name_product = request.form['name_product']
        product.type_product = request.form['type_product']
        product.amount_product = request.form['amount_product']
        product.id_shop = request.form['id_shop']
        product.price_product = request.form['price_product']
        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "При редактировании произошла ошибка!"
    else:
        return render_template("product_edit.html", product=product)


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
            db.session.rollback()
            return db.session.commit()
    else:
        return render_template("products_create.html")