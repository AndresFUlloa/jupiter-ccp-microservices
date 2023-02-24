from microservicio_consul_2 import create_app
from .modelos2 import db, Venta
from .modelos2 import VentaSchema
from flask_restful import Api
from .vistas2 import VistaVenta, VistaVentas


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


api2 = Api(app)
api2.add_resource(VistaVentas, '/ventas')
api2.add_resource(VistaVenta, '/venta/<int:id_venta>')
"""

#prueba
with app.app_context():
    venta_schema = VentaSchema()
    v = Venta(nombre='Roberto Amin', direccion='la calleja', telefono='300200000', producto='bicicleta', pago='efectivo')
    db.session.add(v)
    db.session.commit()
    print([venta_schema.dumps(venta) for venta in Venta.query.all()])
"""