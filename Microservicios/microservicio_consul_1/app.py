from microservicio_consul_1 import create_app
from .modelos import db, Venta, Vendedor, TipoDocumento
from .modelos import VentaSchema, VendedorSchema
from flask_restful import Api
from .vistas import VistaVenta, VistaVentas


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaVentas, '/ventas')
api.add_resource(VistaVenta, '/venta/<int:id_venta>')

"""
#prueba
with app.app_context():
    venta_schema = VentaSchema()
    vendedor_schema = VendedorSchema()
    r = Vendedor(nombre='Erick', apellido='Sanchez', tipo_documento=TipoDocumento.CEDULA, numero_documento='10040004', telefono='3004040400')
    v = Venta(producto='Bicicleta', cantidad=5, cliente='Roberto Amin', vendedor=r.id)
    r.ventas.append(v)
    db.session.add(v)
    db.session.add(r)
    db.session.commit()
    print([venta_schema.dumps(venta) for venta in Venta.query.all()])
    print([vendedor_schema.dumps(vendedor) for vendedor in Vendedor.query.all()])
"""