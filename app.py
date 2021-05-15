from products import *
from shops import *
from orders import *
from employees import *
from sales import *


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        usr = db.session.execute(f"SELECT password from Users where name='{name}'").fetchall()
        if int(password) == int(usr[0][0]):
            return redirect('/main')
        else:
            return "Доступ не разрешен"
    else:
        return render_template("enter.html")

@app.route('/main')
def main():
    return render_template("main_page.html")


if __name__ == "__main__":
    app.run(debug=True)
