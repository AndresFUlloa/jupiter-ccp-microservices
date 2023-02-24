from microservicio_consul_1 import create_app
from .modelos import db, Venta
from .modelos import VentaSchema
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
    v = Venta(nombre='Roberto Amin', direccion='la calleja', telefono='300200000', producto='bicicleta', pago='efectivo')
    db.session.add(v)
    db.session.commit()
    print([venta_schema.dumps(venta) for venta in Venta.query.all()])
"""