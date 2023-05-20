import base64
from typing import List

from flask_restful import Resource
from data import db_session
from flask import jsonify, request

from data.clothes import Clothes
from data.looks import Looks
from data.season import Season
from data.style import Style
from data.type import Type
from data.users import Users


class GetAllLooks(Resource):
    @staticmethod
    def post():
        to_return = []

        session = db_session.create_session()
        user: Users = session.query(Users).filter(Users.id == request.json["user_id"]).first()
        looks: List[Looks] = session.query(Looks).filter(Looks.sex == user.sex | Looks.sex == 3)

        for look in looks:
            style: Style = session.query(Style).filter(Style.id == look.style).first()
            season: Season = session.query(Season).filter(Season.id == look.season).first()

            all_clothes = []

            for clothes in look.clothes:
                clothes_type: Type = session.query(Type).filter(Type.id == clothes.type).first()

                all_clothes.append({
                    "id": clothes.id,
                    "name": clothes.name,
                    "season": {
                        "id": season.id,
                        "name": season.season,
                        "look_season": season.look_season
                    },
                    "type": {
                        "id": clothes_type.id,
                        "name": clothes_type.type
                    },
                    "image": base64.b64encode(open(f"./static/img/clothes_def/{item.image}", "rb").read()).decode(
                        "utf-8"),
                })

            to_return.append({
                "id": look.id,
                "style": {
                    "id": style.id,
                    "name": style.style
                },
                "season": {
                    "id": season.id,
                    "name": season.season,
                    "look_season": season.look_season
                },
                "sex": look.sex,
                "description": look.description,
                "clothes": all_clothes
            })

        return jsonify(to_return)
