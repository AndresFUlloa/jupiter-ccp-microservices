from modelos.modelos import db, Producto, ProductoSchema, Entrada, EntradaSchema
from flask_restful import Api
from flask_cors import CORS
from vistas.vistas import VistaProducto, VistaEntrada, VistaActualizarVenta, VistaProductos
from flask import request
from flask_jwt_extended import JWTManager
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app, resources={r"*": {"origins": "*"}}, origin=['*', 'http://0.0.0.0', 'http://localhost', 'http://127.0.0.1/', 'localhost'])

api = Api(app)
api.add_resource(VistaProducto, '/producto', '/producto/<int:id_producto>')
api.add_resource(VistaProductos, '/productos')
api.add_resource(VistaEntrada, '/entrada')
api.add_resource(VistaActualizarVenta, '/actualizar_venta/<int:venta_id>')

jwt = JWTManager(app)