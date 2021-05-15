from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Orders

@app.route('/orders')
def orders():
    usr = db.session.execute(f"SELECT COUNT(id_user) from Users where access='Yes'").fetchall()
    if usr[0][0] != 0:
        if "action" in request.args:
            if request.args["action"] == "del":  # для обратобки кнопки delete
                id_order = request.args['id']
                order = Orders.query.get_or_404(id_order)

                try:
                    db.session.delete(order)
                    db.session.commit()
                    return redirect("/orders")
                except:
                    return "При удалении записи произошла ошибка"
            elif request.args["action"] == "choice":
                id_product_lst = [request.args['id_product']]
                numb_order_lst = [request.args['numb_order']]
                amount_order_lst = [request.args['amount_order']]
                provider_order_lst = [request.args['provider_order']]
                price_order_lst = [request.args['price_order']]
                date_order_lst = [request.args['date_order']]

                if request.args['id_product'] == "any":
                    temp = db.session.execute(f"SELECT id_product from Orders").fetchall()
                    id_product_lst = [temp[i][0] for i in range(len(temp))]
                if request.args['numb_order'] == "any":
                    temp = db.session.execute(f"SELECT numb_order from Orders").fetchall()
                    numb_order_lst = [temp[i][0] for i in range(len(temp))]
                if request.args['amount_order'] == "any":
                    temp = db.session.execute(f"SELECT amount_order from Orders").fetchall()
                    amount_order_lst = [temp[i][0] for i in range(len(temp))]
                if request.args['provider_order'] == "any":
                    temp = db.session.execute(f"SELECT provider_order from Orders").fetchall()
                    provider_order_lst = [temp[i][0] for i in range(len(temp))]
                if request.args['price_order'] == "any":
                    temp = db.session.execute(f"SELECT price_order from Orders").fetchall()
                    price_order_lst = [temp[i][0] for i in range(len(temp))]
                if request.args['date_order'] == "any":
                    temp = db.session.execute(f"SELECT date_order from Orders").fetchall()
                    date_order_lst = [temp[i][0] for i in range(len(temp))]

                table = db.session.query(Orders) \
                    .filter(Orders.id_product.in_(id_product_lst)) \
                    .filter(Orders.numb_order.in_(numb_order_lst)) \
                    .filter(Orders.amount_order.in_(amount_order_lst)) \
                    .filter(Orders.provider_order.in_(provider_order_lst)) \
                    .filter(Orders.price_order.in_(price_order_lst)) \
                    .filter(Orders.date_order.in_(date_order_lst))
                return render_template("orders.html", table=table)
            elif request.args["action"] == "first":
                table = db.session.execute(f"select * from Orders as O "
                                           f"INNER JOIN products as pr "
                                           f"ON O.id_product = pr.id_product"
                                           f" and O.amount_order > {request.args['numb']}"
                                           f" and type_product = '{request.args['type']}'").fetchall()
                return render_template("orders.html", table=table)
            else:
                return redirect("/orders")
        else:
            table = Orders.query.order_by(Orders.id_order).all()
            return render_template("orders.html", table=table)
    else:
        return render_template("denied.html")


@app.route('/order-choice', methods=['POST'])
def order_choice():
    return redirect(f"/orders?action=choice"
                    f"&id_product={request.form['id_product']}"
                    f"&numb_order={request.form['numb_order']}"
                    f"&amount_order={request.form['amount_order']}"
                    f"&provider_order={request.form['provider_order']}"
                    f"&price_order={request.form['price_order']}"
                    f"&date_order={request.form['date_order']}")

@app.route('/orders/first', methods=['POST'])
def order_first():
    return redirect(f"/orders?action=first"
                    f"&numb={request.form['numb']}"
                    f"&type={request.form['type']}")


@app.route('/orders/<int:id>/edit', methods=['POST', 'GET'])
def edit_order(id):
    order = Orders.query.get_or_404(id)
    if request.method == "POST":
        order.id_product = request.form['id_product']
        order.numb_order = request.form['numb_order']
        order.amount_order = request.form['amount_order']
        order.provider_order = request.form['provider_order']
        order.price_order = request.form['price_order']
        order.date_order = request.form['date_order']
        try:
            db.session.commit()
            return redirect('/orders')
        except:
            return "При редактировании произошла ошибка!"
    else:
        return render_template("order_edit.html", order=order)

@app.route('/orders/create', methods=['POST', 'GET'])
def create_order():
    if request.method == "POST":
        id_product = request.form['id_product']
        numb_order = request.form['numb_order']
        amount_order = request.form['amount_order']
        provider_order = request.form['provider_order']
        price_order = request.form['price_order']
        date_order = request.form['date_order']


        orders = Orders(id_product=id_product, numb_order=numb_order, amount_order=amount_order,
                        provider_order=provider_order, price_order=price_order, date_order=date_order)

        db.session.add(orders)
        try:
            db.session.commit()
            return redirect('/orders')
        except:
            return db.session.commit()
    else:
        return render_template("orders_create.html")