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
                "name": item.name,
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


class GetClothesInfoResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        types = session.query(Type).all()
        seasons = session.query(Season).all()

        return jsonify({
            "types": [{"id": t.id, "name": t.type} for t in types],
            "seasons": [{"id": s.id, "name": s.season, "look_season": s.look_season} for s in seasons],
        })


class GetClothesFromWardrobeResource(Resource):
    @staticmethod
    def post():
        to_return = []
        session = db_session.create_session()

        clothes_type = session.query(Type).filter(Type.id == request.json["type_id"]).first()
        clothes_season = session.query(Season).filter(Season.id == request.json["season_id"]).first()
        all_clothes = session.query(Clothes).filter(Clothes.type == clothes_type.id,
                                                    Clothes.season == clothes_season.id)

        for clothes in all_clothes:
            to_return.append({
                "id": clothes.id,
                "name": clothes.name,
                "image": base64.b64encode(open(f"./static/img/clothes_def/{clothes.image}", "rb").read()).decode(
                    "utf-8"),
                "type": {
                    "id": clothes_type.id,
                    "name": clothes_type.type
                },
                "season": {
                    "id": clothes_season.id,
                    "name": clothes_season.season,
                    "look_season": clothes_season.look_season
                },
            })

        return jsonify(to_return)


class SetClothesInWardrobe(Resource):
    @staticmethod
    def post():
        session = db_session.create_session()
        user = session.get(Users, request.json["user_id"])
        user.clothes.append(session.get(Clothes, request.json["clothes_id"]))
        session.commit()
