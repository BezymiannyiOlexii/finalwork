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
