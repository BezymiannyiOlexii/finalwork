from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Sales

@app.route('/sales')
def sales():
    if "action" in request.args:
        if request.args["action"] == "del":  # для обратобки кнопки delete
            id_sale = request.args['id']
            sale = Sales.query.get_or_404(id_sale)

            try:
                db.session.delete(sale)
                db.session.commit()
                return redirect("/sales")
            except:
                return "При удалении записи произошла ошибка"
        elif request.args["action"] == "choice":
            id_product_lst = [request.args['id_product']]
            id_employee_lst = [request.args['id_employee']]
            id_shop_lst = [request.args['id_shop']]
            amount_sale_lst = [request.args['amount_sale']]
            date_sale_lst = [request.args['date_sale']]
            name_buyer_lst = [request.args['name_buyer']]
            text_buyer_lst = [request.args['text_buyer']]

            if request.args['id_product'] == "any":
                temp = db.session.execute(f"SELECT id_product from Sales").fetchall()
                id_product_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['id_employee'] == "any":
                temp = db.session.execute(f"SELECT id_employee from Sales").fetchall()
                id_employee_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['id_shop'] == "any":
                temp = db.session.execute(f"SELECT id_shop from Sales").fetchall()
                id_shop_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['amount_sale'] == "any":
                temp = db.session.execute(f"SELECT amount_sale from Sales").fetchall()
                amount_sale_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['date_sale'] == "any":
                temp = db.session.execute(f"SELECT date_sale from Sales").fetchall()
                date_sale_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['name_buyer'] == "any":
                temp = db.session.execute(f"SELECT name_buyer from Sales").fetchall()
                name_buyer_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['text_buyer'] == "any":
                temp = db.session.execute(f"SELECT text_buyer from Sales").fetchall()
                text_buyer_lst = [temp[i][0] for i in range(len(temp))]

            table = db.session.query(Sales) \
                .filter(Sales.id_product.in_(id_product_lst)) \
                .filter(Sales.id_employee.in_(id_employee_lst)) \
                .filter(Sales.id_shop.in_(id_shop_lst)) \
                .filter(Sales.amount_sale.in_(amount_sale_lst)) \
                .filter(Sales.date_sale.in_(date_sale_lst)) \
                .filter(Sales.name_buyer.in_(name_buyer_lst)) \
                .filter(Sales.text_buyer.in_(text_buyer_lst))
            return render_template("sales.html", table=table)
        else:
            return redirect("/sales")
    else:
        table = Sales.query.order_by(Sales.id_sale).all()
        return render_template("Sales.html", table=table)


@app.route('/sale-choice', methods=['POST'])
def sale_choice():
    return redirect(f"/sales?action=choice"
                    f"&id_product={request.form['id_product']}"
                    f"&id_employee={request.form['id_employee']}"
                    f"&id_shop={request.form['id_shop']}"
                    f"&amount_sale={request.form['amount_sale']}"
                    f"&date_sale={request.form['date_sale']}"
                    f"&name_buyer={request.form['name_buyer']}"
                    f"&text_buyer={request.form['text_buyer']}")


@app.route('/sales/<int:id>/edit', methods=['POST', 'GET'])
def edit_sale(id):
    sale = Sales.query.get_or_404(id)
    if request.method == "POST":
        sale.id_product = request.form['id_product']
        sale.id_employee = request.form['id_employee']
        sale.id_shop = request.form['id_shop']
        sale.amount_sale = request.form['amount_sale']
        sale.date_sale = request.form['date_sale']
        sale.name_buyer = request.form['name_buyer']
        sale.text_buyer = request.form['text_buyer']
        try:
            db.session.commit()
            return redirect('/sales')
        except:
            return "При редактировании произошла ошибка!"
    else:
        return render_template("sale_edit.html", sale=sale)

@app.route('/sales/create', methods=['POST', 'GET'])
def create_sale():
    if request.method == "POST":
        id_product = request.form['id_product']
        id_employee = request.form['id_employee']
        id_shop = request.form['id_shop']
        amount_sale = request.form['amount_sale']
        date_sale = request.form['date_sale']
        name_buyer = request.form['name_buyer']
        text_buyer = request.form['text_buyer']


        sales = Sales(id_product=id_product, id_employee=id_employee, id_shop=id_shop,
                        amount_sale=amount_sale, date_sale=date_sale, name_buyer=name_buyer, text_buyer=text_buyer)

        db.session.add(sales)
        try:
            db.session.commit()
            return redirect('/sales')
        except:
            db.session.rollback()
            return db.session.commit()
    else:
        return render_template("sales_create.html")