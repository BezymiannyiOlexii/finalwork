from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Employees


@app.route('/employees')
def employees():
    if "action" in request.args:
        if request.args["action"] == "del": #для обратобки кнопки delete
            id_employee = request.args['id']
            employee = Employees.query.get_or_404(id_employee)

            try:
                db.session.delete(employee)
                db.session.commit()
                return redirect("/employees")
            except:
                return "При удалении записи произошла ошибка"
        elif request.args["action"] == "choice":
            id_employee_lst = [request.args['id_employee']]
            name_employee_lst = [request.args['name_employee']]
            id_shop_lst = [request.args['id_shop']]
            salary_lst = [request.args['salary']]

            if request.args['id_employee'] == "any":
                temp = db.session.execute(f"SELECT id_employee from Employees").fetchall()
                id_employee_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['name_employee'] == "any":
                temp = db.session.execute(f"SELECT name_employee from Employees").fetchall()
                name_employee_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['id_shop'] == "any":
                temp = db.session.execute(f"SELECT id_shop from Employees").fetchall()
                id_shop_lst = [temp[i][0] for i in range(len(temp))]
            if request.args['salary'] == "any":
                temp = db.session.execute(f"SELECT salary from Employees").fetchall()
                salary_lst = [temp[i][0] for i in range(len(temp))]

            table = db.session.query(Employees).filter(Employees.id_employee.in_(id_employee_lst))\
                .filter(Employees.name_employee.in_(name_employee_lst))\
                .filter(Employees.id_shop.in_(id_shop_lst))\
                .filter(Employees.salary.in_(salary_lst))
            return render_template("Employees.html", table=table)


        else:
            return redirect("/employees")
    else:
        table = Employees.query.order_by(Employees.id_employee).all()
        return render_template("employees.html", table=table)


@app.route('/employee-choice', methods =['POST'])
def employee_choice():

    return redirect(f"/employees?action=choice&id_employee={request.form['id_employee']}"
                    f"&name_employee={request.form['name_employee']}&id_shop={request.form['id_shop']}"
                    f"&salary={request.form['salary']}")

@app.route('/employees/<int:id>/edit', methods=['POST', 'GET'])
def edit_employee(id):
    employee = Employees.query.get_or_404(id)
    if request.method == "POST":
        employee.name_employee = request.form['name_employee']
        employee.id_shop = request.form['id_shop']
        employee.salary = request.form['salary']
        try:
            db.session.commit()
            return redirect('/employees')
        except:
            return "При редактировании произошла ошибка!"
    else:
        return render_template("employee_edit.html", employee=employee)
    

@app.route('/employees/create', methods=['POST', 'GET'])
def create_employee():
    if request.method == "POST":
        name_employee = request.form['name_employee']
        id_shop = request.form['id_shop']
        salary = request.form['salary']

        employees = Employees(name_employee=name_employee, id_shop=id_shop, salary=salary)

        try:
            db.session.add(employees)
            db.session.commit()
            return redirect('/employees')
        except:
            db.session.rollback()
            return "Произошла ошибка!"
    else:
        return render_template("employee_create.html")