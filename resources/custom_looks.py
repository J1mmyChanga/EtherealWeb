import base64

from flask_restful import Resource
from data import db_session
from flask import jsonify, request

from data.looks import Looks
from data.season import Season
from data.style import Style
from data.type import Type
from data.users import Users


class GetCustomLooksResource(Resource):
    styles = {2: "casual", 1: "business", 3: "sportswear"}

    @classmethod
    def post(cls):
        to_return = {"casual": [], "business": [], "sportswear": []}

        session = db_session.create_session()
        user = session.get(Users, request.json["user_id"])

        for look in session.query(Looks).filter((Looks.sex == user.sex) | (Looks.sex == 3)):
            clothes_list = []
            look: Looks
            for clothes in look.clothes:
                if clothes not in user.clothes:
                    break
                clothes_list.append(clothes)

            if len(clothes_list) >= 2:
                style = session.get(Style, look.style)
                season = session.get(Season, look.season)
                all_clothes = []

                for clothes in look.clothes:
                    clothes_type = session.get(Type, clothes.type)

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
                        "image": base64.b64encode(
                            open(f"./static/img/clothes_def/{clothes.image}", "rb").read()).decode(
                            "utf-8"),
                    })

                to_return[cls.styles[look.style]].append({
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
                    "description": look.description if look.description is not None else "",
                    "clothes": all_clothes
                })

        return jsonify(to_return)
