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
    # date = db.Column(db.DataTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Products %r' % self.id_product
