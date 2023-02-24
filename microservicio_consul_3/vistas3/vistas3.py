from flask_restful import Resource
from ..modelos3 import db, Venta, VentaSchema
from flask import request

venta_schema = VentaSchema()

class VistaVentas(Resource):
    def get(self):
        return [venta_schema.dump(venta) for venta in Venta.query.all()]

class VistaVenta(Resource):
    def get(self, id_venta):
        return venta_schema.dump(Venta.query.get_or_404(id_venta))

