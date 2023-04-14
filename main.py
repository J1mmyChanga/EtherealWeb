from flask import Flask
from data import db_session
from data.clothes import Clothes
from data.functionality import Functionality
from data.looks import Looks
from data.season import Season
from data.style import Style
from data.type import Type
from data.users import Users

app = Flask(__name__)

def main():
    db_session.global_init('db/ethereal.db')
    session = db_session.create_session()
    user = session.get(Users, 1)
    user.clothes.clear()
    session.commit()


if __name__ == '__main__':
    main()