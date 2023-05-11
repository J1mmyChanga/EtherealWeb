import base64

from flask_restful import Resource
from data import db_session
from flask import jsonify, request

from data.clothes import Clothes
from data.season import Season
from data.type import Type
from data.users import Users


class WardrobeResource(Resource):
    @staticmethod
    def post():
        to_return = []
        session = db_session.create_session()
        user: Users = session.query(Users).filter(Users.id == request.json["user_id"]).first()

        for item in user.clothes:
            item: Clothes
            clothes_type: Type = session.query(Type).filter(Type.id == item.type).first()
            clothes_season: Season = session.query(Season).filter(Season.id == item.season).first()

            to_return.append({
                "id": item.id,
                "image": base64.b64encode(open(f"./static/img/clothes_def/{item.image}", "rb").read()).decode("utf-8"),
                "type": {
                    "id": clothes_type.id,
                    "name": clothes_type.type
                },
                "season": {
                    "id": clothes_season.id,
                    "name": clothes_season.season,
                    "look_season": clothes_season.look_season
                }
            })

        return jsonify(to_return)
