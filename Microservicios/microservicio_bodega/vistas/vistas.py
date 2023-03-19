import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from faker import Faker

from modelos import *

producto_schema = ProductoSchema()
entrada_schema = EntradaSchema()
data_factory = Faker()

class VistaProductos(Resource):
    @jwt_required()
    def get(self):
        return [producto_schema.dump(producto) for producto in Producto.query.all()]

class VistaProducto(Resource):
    @jwt_required()
    def post(self):
        print(request.json)
        nuevo_producto = Producto(
            codigo=request.json['codigo'],
            descripcion=request.json['descripcion'],
            precio=request.json['precio'],
            stock = 0,
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return {
            'producto': producto_schema.dumps(nuevo_producto),
            'message': 'Producto creado exitosamente' }, 200

    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.codigo = request.json['codigo'],
        producto.descripcion = request.json['descripcion'],
        producto.precio = request.json['precio']
        db.session.add(producto)
        db.session.commit()
        return {
            'producto': producto_schema.dumps(nuevo_producto),
            'message': 'Producto Editado exitosamente' }, 200

    def delete(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        db.session.delete(producto)
        db.session.commit()
        return '', 200

    def get(self, id_producto):
        return producto_schema.dump(Producto.query.get_or_404(id_producto))

class VistaEntrada(Resource):

    def post(self):
        producto = Producto.query.get_or_404(request.json['id_producto'])
        nueva_entrada = Entrada(
           cantidad = request.json['cantidad']
        )
        producto.entradas.append(nueva_entrada)
        producto.stock += nueva_entrada.cantidad
        db.session.add(nueva_entrada)
        db.session.add(nueva_entrada)
        db.session.commit()
        return '', 200


class VistaActualizarVenta(Resource):
    @jwt_required()
    def post(self, venta_id):
        venta = Venta.query.get_or_404(venta_id)
        print(request)
        producto = Producto.query.get_or_404(request.json['producto_id'])
        producto.ventas.append(venta)
        producto.stock -= venta.cantidad
        db.session.commit()
        return "", 200



