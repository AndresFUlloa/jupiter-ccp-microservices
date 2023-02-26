from microservicio_consul_3 import create_app
from .modelos3 import db, Venta, Vendedor, TipoDocumento
from .modelos3 import VentaSchema, VendedorSchema
from flask_restful import Api
from .vistas3 import VistaVenta, VistaVentas
from flask import request
from flask import Flask

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api3 = Api(app)
api3.add_resource(VistaVentas, '/ventas')
api3.add_resource(VistaVenta, '/venta/<int:id_venta>')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    func()
