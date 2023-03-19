import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import pika
from cola_mensajes.utiles.exchange_util import ExchangeUtil

class VistaVentaInventario(Resource):
    @jwt_required()
    def post(self):
        ExchangeUtil.start_connection()
        ExchangeUtil.send_message(request.json)
        ExchangeUtil.close_connection()
        return 'Solicitud encolada', 200

