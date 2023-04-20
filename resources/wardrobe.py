import base64

from flask_restful import Resource
from data import db_session
from flask import jsonify, request

from data.clothes import Clothes
from data.users import Users


class WardrobeResource(Resource):
    @staticmethod
    def post():
        to_return = []
        session = db_session.create_session()
        user: Users = session.query(Users).filter(Users.id == request.json["user_id"]).first()

        for item in user.clothes:
            item: Clothes
            to_return.append({
                "id": item.id,
                "image": base64.b64encode(open(f"../static/img/clothes_def/{item.image}", "rb").read()).decode("utf-8"),
                "type": {
                    "id": item.type.id,
                    "name": item.type.type
                },
                "season": {
                    "id": item.season.id,
                    "name": item.season.season,
                    "look_season": item.season.look_season
                }
            })
        return jsonify(to_return)
