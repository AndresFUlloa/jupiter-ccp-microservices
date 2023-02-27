from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import backref
from enum import Enum

db = SQLAlchemy()


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave': value.name, 'valor': value.value}


class TipoDocumento(Enum):
    CEDULA = 1
    TARJETA_IDENTIDAD = 2
    PASAPORTE = 3
    CEDULA_EXTRANJERIA = 4


class Vendedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido = db.Column(db.String(128))
    tipo_documento = db.Column(db.Enum(TipoDocumento))
    numero_documento = db.Column(db.String(32))
    telefono = db.Column(db.String(16))
    ventas = db.relationship('Venta', cascade='all, delete, delete-orphan')


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(128))
    cantidad = db.Column(db.Integer)
    cliente = db.Column(db.String(64))
    vendedor = db.Column(db.Integer, db.ForeignKey('vendedor.id'))


class VendedorSchema(SQLAlchemyAutoSchema):
    tipo_documento = EnumADiccionario(attribute=('tipo_documento'))

    class Meta:
        model = Vendedor
        include_relationships = True
        load_instance = True

    id = fields.String()


class VentaSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Venta
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.String()
