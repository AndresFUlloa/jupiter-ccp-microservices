import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from faker import Faker
import requests

from VentasCommand.modelos.modelos import *

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

@jwt_required()
class VistaVenta(Resource):

    def post(self, id_vendedor):
        vendedor = Vendedor.query.get_or_404(id_vendedor)
        nueva_venta = Venta(
            cantidad=request.json['cantidad'],
            cliente=request.json['cliente'],
            factura=request.json['factura'],
            vendedor=vendedor.id
        )
        vendedor.ventas.append(nueva_venta)
        db.session.add(nueva_venta)
        db.session.add(vendedor)
        db.session.commit()
        requests.post('http://127.0.0.1:5007/venta_inventario',json={'venta_id':nueva_venta.id, 'producto_id':request.json['producto_id']})
        return '', 200

    def put(self, id_venta):
        venta = Venta.query.get_or_404(id_venta)
        venta.producto = request.json['producto'],
        venta.cantidad = request.json['cantidad'],
        venta.cliente = request.json['cliente'],
        venta.factura = request.json['factura'],
        venta.vendedor = request.json['vendedor']
        db.session.add(venta)
        db.session.commit()
        return '', 200

    def delete(self, id_venta):
        venta = Venta.query.get_or_404(id_venta)
        db.session.delete(venta)
        db.session.commit()
        return '', 200

