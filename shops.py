from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Shops


@app.route('/shops')
def shops():
    if "action" in request.args:
        if request.args["action"] == "del": #для обратобки кнопки delete
            id_shop = request.args['id']
            shop = Shops.query.get_or_404(id_shop)

            try:
                db.session.delete(shop)
                db.session.commit()
                return redirect("/shops")
            except:
                return "При удалении записи произошла ошибка"
        elif request.args["action"] == "choice":
            id_lst = [request.args['id_shop']]
            type_shop_lst = [request.args['type_shop']]
            shops_area_lst = [request.args['shops_area']]
            hall_count_lst = [request.args['hall_count']]
            stall_count_lst = [request.args['stall_count']]

            if request.args['id_shop'] == "any":
                temp = db.session.execute(f"SELECT id_shop from Shops").fetchall()
                id_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['type_shop'] == "any":
                temp = db.session.execute(f"SELECT type_shop from Shops").fetchall()
                type_shop_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['shops_area'] == "any":
                temp = db.session.execute(f"SELECT shops_area from Shops").fetchall()
                shops_area_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['hall_count'] == "any":
                temp = db.session.execute(f"SELECT hall_count from Shops").fetchall()
                hall_count_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['stall_count'] == "any":
                temp = db.session.execute(f"SELECT stall_count from Shops").fetchall()
                stall_count_lst = [temp[i][0] for i in range(len(temp))]

            table = db.session.query(Shops).filter(Shops.id_shop.in_(id_lst)).filter(Shops.type_shop.in_(type_shop_lst)).filter(Shops.shops_area.in_(shops_area_lst)).filter(Shops.hall_count.in_(hall_count_lst)).filter(Shops.stall_count.in_(stall_count_lst ))
            return render_template("shops.html", table=table)


        else:
            return redirect("/shops")
    else:
        table = Shops.query.order_by(Shops.id_shop).all()
        #table = Shops.query.filter_by(type_shop="Магазин").filter_by(id_shop=1).all()
        #table = Shops.query.all()
        #table = Shops.query.filter_by(Shops.id_shop in [1,2]).all()
        return render_template("shops.html", table=table)


@app.route('/shop-choice', methods =['POST'])
def shop_choice():
    '''При выборе елеменетов для вывода эта функция принимает значения выпадающего меню методом POST
    и возвращает для обработки методом GET, через параметры ссылки в /shops '''
    return redirect(f"/shops?action=choice&id_shop={request.form['id_shop']}&type_shop={request.form['type_shop']}&shops_area={request.form['shops_area']}&hall_count={request.form['hall_count']}&stall_count={request.form['stall_count']}")

@app.route('/shops/<int:id>/edit', methods=['POST', 'GET'])
def edit_shop(id):
    shop = Shops.query.get_or_404(id)
    if request.method == "POST":
        shop.type_shop = request.form['type_shop']
        shop.shops_area = request.form['shops_area']
        shop.hall_count = request.form['hall_count']
        shop.stall_count = request.form['stall_count']
        try:
            db.session.commit()
            return redirect('/shops')
        except:
            return "При редактировании произошла ошибка!"
    else:
        return render_template("shop_edit.html", shop=shop)



@app.route('/shops/create', methods=['POST', 'GET'])
def create_shop():
    if request.method == "POST":
        type_shop = request.form['type_shop']
        shops_area = request.form['shops_area']
        hall_count = request.form['hall_count']
        stall_count = request.form['stall_count']

        shops = Shops(type_shop=type_shop, shops_area=shops_area, hall_count=hall_count, stall_count=stall_count)

        try:
            db.session.add(shops)
            db.session.commit()
            return redirect('/shops')
        except:
            return "Произошла ошибка!"
    else:
        return render_template("shop_create.html")