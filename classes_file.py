from connection_file import db
from datetime import datetime


class Shops(db.Model):
    id_shop = db.Column(db.Integer, primary_key=True)
    type_shop = db.Column(db.String(10), nullable=False)
    shops_area = db.Column(db.Integer, nullable=False)
    hall_count = db.Column(db.Integer, default=1)
    stall_count = db.Column(db.Integer, default=1)
    # date = db.Column(db.DataTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Shops %r' % self.id_shop


class Products(db.Model):
    id_product = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(20), nullable=False)
    type_product = db.Column(db.String(20), nullable=False)
    amount_product = db.Column(db.Integer, nullable=False)
    id_shop = db.Column(db.Integer, nullable=False)
    price_product = db.Column(db.Integer, default=0)

    def __repr__(self):
        return 'Products %r' % self.id_product

class Orders(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, nullable=False)
    numb_order = db.Column(db.Integer, nullable=False)
    amount_order = db.Column(db.Integer, nullable=False)
    provider_order = db.Column(db.String(20), nullable=False)
    price_order = db.Column(db.Integer, default=0)
    date_order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Order %r' % self.id_order

class Employees(db.Model):
    id_employee = db.Column(db.Integer, primary_key=True)
    name_employee = db.Column(db.String(30), nullable=False)
    id_shop = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Employee %r' % self.id_employee

class Sales(db.Model):
    id_sale = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, nullable=False)
    id_employee = db.Column(db.Integer, nullable=False)
    id_shop = db.Column(db.Integer, nullable=False)
    amount_sale = db.Column(db.Integer, nullable=False)
    date_sale = db.Column(db.Integer, nullable=False)
    name_buyer = db.Column(db.String(30), nullable=False)
    text_buyer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Sales %r' % self.id_sale




