from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Shops
from sqlalchemy.sql import select


#def fromSQL_to_Alchemy(lst, clas):


@app.route('/')
def index():
    try:
        return f'ну че погнали ебана в рот!{request.args["id"]}'
    except:
        return redirect("/?id=nrejnoren")


@app.route('/shops')
def shops():
    if "action" in request.args:
        if request.args["action"] == "del":
            id_shop = request.args['id']
            shop = Shops.query.get_or_404(id_shop)

            try:
                db.session.delete(shop)
                db.session.commit()
                return redirect("/shops")
            except:
                return "При удалении записи произошла ошибка"
        else:
            return redirect("/shops")
    else:
        #table = Shops.query.order_by(Shops.id_shop).all()
        #table = Shops.query.filter_by(type_shop="Магазин").filter_by(id_shop=1).all()
        #table = Shops.query.all()
        #table = db.session.execute('SELECT shops.id_shop AS shops_id_shop, shops.type_shop AS shops_type_shop, shops.shops_area AS shops_shops_area, shops.hall_count AS shops_hall_count, shops.stall_count AS shops_stall_count FROM shops')
        #table = db.session.query(Shops).filter(Shops.id_shop == 2)
        str = "'Магазин'"
        table = db.session.execute(f"SELECT * from Shops WHERE type_shop={str}").fetchall()
        return render_template("shops.html", table=table)


@app.route('/shop-choice', methods =['POST'])
def shop_choice():
    return "Here: " + request.form['id_shop'] + request.form['type_shop']

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


if __name__ == "__main__":
    app.run(debug=True)
