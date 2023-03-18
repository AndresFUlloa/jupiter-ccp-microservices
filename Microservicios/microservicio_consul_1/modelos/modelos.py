from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import backref
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

venta_producto_association_table = db.Table(
    "venta_producto_association_table",
    db.metadata,
    db.Column('venta_id', db.Integer, db.ForeignKey('venta.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True)
)

producto_entrada_association_table = db.Table(
    "producto_entrada_association_table",
    db.metadata,
    db.Column('entrada_id', db.Integer, db.ForeignKey('entrada.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True)
)


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
    cantidad = db.Column(db.Integer)
    cliente = db.Column(db.String(64))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    factura = db.Column(db.String(32))
    vendedor = db.Column(db.Integer, db.ForeignKey('vendedor.id'))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(128))
    descripcion = db.Column(db.String(128))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)
    entradas = db.relationship('Entrada', secondary='producto_entrada_association_table', backref='productos_entrada')
    ventas = db.relationship('Venta', secondary='venta_producto_association_table', backref='ventas')

    def valor_inventario(self):
        return self.precio * self.stock

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer)


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

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.String()

class EntradaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entrada
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.String()

