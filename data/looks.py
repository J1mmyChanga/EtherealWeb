import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Looks(SqlAlchemyBase):
    __tablename__ = 'looks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    style = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("style.id"))
    season = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("season.id"))
    first = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("clothes.id"))
    second = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("clothes.id"))
    lower = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("clothes.id"))

    styles = orm.relationship("Style", backref='looks')
    seasons = orm.relationship("Season", backref='looks')
    clothes = orm.relationship("Clothes", backref='looks', foreign_keys=[first])