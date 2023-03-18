import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from celery import Celery
from cola_mensajes.task import process_request

#app_ventas = Celery('task', broker='pyamqp://guest@localhost//')

class VistaVentaInventario(Resource):

    def post(self):
        print(request)
        process_request.delay(request.json['producto_id'])

        return 'Solicitud encolada', 200

