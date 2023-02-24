from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60))
    direccion = db.Column(db.String(120))
    telefono = db.Column(db.String(12))
    producto = db.Column(db.String(120))
    pago = db.Column(db.String(60))

    def __repr__(self):
        return "{}-{}-{}-{}-{}".format(self.nombre, self.direccion, self.telefono, self.producto, self.pago)

class VentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        include_relationships = False
        load_instance = True
