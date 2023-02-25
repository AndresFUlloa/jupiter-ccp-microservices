import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from faker import Faker

from modelos import *

vendedor_schema = VendedorSchema()
venta_schema = VendedorSchema()
data_factory = Faker()


class VistaVendedor(Resource):

    def post(self):
        nuevo_vendedor = Vendedor(
            nombre=request.json['nombre'],
            apellido=request.json['apellido'],
            tipo_documento=request.json['tipo_documento'],
            numero_documento=request.json['numero_documento'],
            telefono=request.json['telefono']
        )
        db.session.add(nuevo_vendedor)
        db.session.commit()
        return {
            'vendedor': vendedor_schema.dumps(nuevo_vendedor),
            'message': 'Vendedor creado exitosamente' }, 200

    def put(self, id_vendedor):
        vendedor = Vendedor.query.get_or_404(id_vendedor)
        vendedor.nombre = request.json['nombre']
        vendedor.apellido = request.json['apellido']
        vendedor.tipo_documento = request.json['tipo_documento']
        vendedor.numero_documento = request.json['numero_documento']
        vendedor.telefono = request.json['telefono']

        db.session.add(vendedor)
        db.session.commit()
        return {
            'Vendedor': vendedor_schema.dumps(vendedor),
            'message': 'Vendedor Editado'}, 200

    def delete(self, id_vendedor):
        vendedor = Vendedor.query.get_or_404(id_vendedor)
        db.session.delete(vendedor)
        db.session.commit()
        return '', 200


class VistaVenta(Resource):

    def post(self, id_vendedor):
        vendedor = Vendedor.query.get_or_404(id_vendedor)
        nueva_venta = Venta(
            producto=request.json['producto'],
            cantidad=request.json['cantidad'],
            cliente=request.json['cliente'],
            vendedor=vendedor.id
        )
        vendedor.ventas.append(nueva_venta)
        db.session.add(nueva_venta)
        db.session.add(vendedor)
        db.commit()
        return '', 200

    def put(self, id_venta):
        venta = Venta.query.get_or_404(id_venta)
        venta.producto = request.json['producto'],
        venta.cantidad = request.json['cantidad'],
        venta.cliente = request.json['cliente'],
        venta.vendedor = request.json['vendedor']
        db.session.add(venta)
        db.session.commit()
        return '', 200

    def delete(self, id_venta):
        venta = Venta.query.get_or_404(id_venta)
        db.session.delete(venta)
        db.session.commit()
        return '', 200


class VistaPruebas(Resource):

    def get(self):
        nuevo_vendedor = Vendedor(
            nombre=data_factory.name(),
            apellido=data_factory.last_name(),
            tipo_documento=TipoDocumento.CEDULA,
            numero_documento=str(data_factory.pyint(min_value=1000000000, max_value=9999999999)),
            telefono=str(data_factory.pyint(min_value=1000000000, max_value=9999999999))
        )
        db.session.add(nuevo_vendedor)
        db.session.commit()

        nueva_venta = Venta(
            producto=data_factory.word(),
            cantidad=data_factory.pyint(min_value=1, max_value=5000),
            cliente='{} {}'.format(data_factory.name(), data_factory.last_name()),
            vendedor=nuevo_vendedor.id
        )
        db.session.add(nueva_venta)
        db.session.commit()

        db.session.delete(nueva_venta)
        db.session.delete(nuevo_vendedor)
        return 'Prueba Exitosa', 200
    