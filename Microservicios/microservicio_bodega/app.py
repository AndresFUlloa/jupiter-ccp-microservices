from modelos.modelos import db, Producto, ProductoSchema, Entrada, EntradaSchema
from flask_restful import Api
from vistas.vistas import VistaProducto, VistaEntrada
from flask import request
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

api = Api(app)
api.add_resource(VistaProducto, '/producto', '/producto/<int:id_producto>')
api.add_resource(VistaEntrada, '/entrada')