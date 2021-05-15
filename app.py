from products import *
from shops import *
from orders import *
from employees import *
from sales import *
from classes_file import Users


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        usr = db.session.execute(f"SELECT * from Users where name='{name}'").fetchall()
        if int(password) == int(usr[0][2]):
            usr_1 = Users.query.get_or_404(usr[0][0])
            usr_1.access = 'Yes'
            db.session.commit()
            return redirect('/main')
        else:
            return render_template("denied.html")
    else:
        return render_template("enter.html")

@app.route('/exit')
def exit():
    usr_1 = Users.query.get_or_404(1)
    usr_1.access = 'No'
    db.session.commit()
    return redirect('/')

@app.route('/main')
def main():
    return render_template("main_page.html")


if __name__ == "__main__":
    app.run(debug=True)
