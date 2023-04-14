import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)

    looks = orm.relationship("Looks",
                            secondary="user_to_favourite",
                            backref="users")

    clothes = orm.relationship("Clothes",
                             secondary="user_to_clothes",
                             backref="users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)