from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum

from sqlalchemy.orm import backref

db = SQLAlchemy()


class TipoUsuario(Enum):
    ADMINISTRADOR = 1
    VENDEDOR = 2
    INVENTARIO = 3


class Miscroservicios(Enum):
    VENTAS = 1
    INVENTARIO = 2


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    tipo_usuario = db.Column(db.Enum(TipoUsuario))
    email = db.Column(db.String(256))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave': value.name, 'valor': value.value}


class UsuarioSchema(SQLAlchemyAutoSchema):
    tipo_usuario = EnumADiccionario(attribute=('tipo_usuario'))

    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

    id = fields.String()
