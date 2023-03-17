import flask
import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import hashlib

from modelos import *

usuario_schema = UsuarioSchema()

class VistaSignIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json['usuario']).first()
        if usuario is not None:
            return 'El usuario {} ya existe'.format(usuario.usuario), 409

        usuario = Usuario.query.filter(Usuario.email == request.json['email']).first()
        if usuario is not None:
            return 'Ya existe un usuario con email: {}'.format(usuario.email), 409

        contrasena = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        nuevo_usuario = Usuario(
            usuario=request.json['usuario'],
            contrasena=contrasena,
            tipo_usuario=request.json['tipo_usuario'],
            email=request.json['email']
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        dict_usuario = usuario_schema.dump(nuevo_usuario)
        del dict_usuario['contrasena']

        return dict_usuario, 200


class VistaLogIn(Resource):

    def post(self):
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()

        if usuario is None:
            return 'El usuario no existe', 404

        token_de_acceso = create_access_token(identity=usuario.id)
        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token_de_acceso,
            "id": usuario.id,
            "tipo_usuario": usuario.tipo_usuario.value
        }, 200

class VistaValidation(Resource):

    @jwt_required()
    def get(self, microservicio):
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.get_or_404(id_usuario)

        if usuario.tipo_usuario == TipoUsuario.VENDEDOR:
            if Miscroservicios.INVENTARIO.value == microservicio:
                return 'Usuario no tiene acceso', 403
        elif usuario.tipo_usuario == TipoUsuario.INVENTARIO:
            if Miscroservicios.VENTAS.value == microservicio:
                return 'Usuario no tiene acceso', 403

        return {
            "mensaje": "Usuario valido",
            "id": id_usuario,
            "tipo_usuario": usuario.tipo_usuario.value,
            "nombre_ususario": usuario.usuario
        }, 200