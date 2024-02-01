import base64

from flask_restful import Resource
from data import db_session
from flask import jsonify, request

from data.sex import Sex
from data.users import Users


class RegisterResource(Resource):
    @staticmethod
    def post():
        nickname = request.json["nickname"]
        password = request.json["password"]
        email = request.json["email"]

        session = db_session.create_session()
        user = Users(
            nickname=nickname,
            email=email,
            sex=session.query(Sex).first(),
        )
        user.set_password(password)
        session.add(user)
        session.commit()

        return jsonify("success")
