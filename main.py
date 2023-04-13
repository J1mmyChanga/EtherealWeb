from flask import Flask
from data import db_session
from data.functionality import Functionality
from data.season import Season
from data.style import Style
from data.type import Type

app = Flask(__name__)

def main():
    db_session.global_init('db/ethereal.db')
    session = db_session.create_session()
    season1 = Season(id=1, season='Лето', look_season='Летний')
    session.add(season1)
    # season2 = Season(id=2, season='Зима', look_season='Зимний')
    # session.add(season2)
    # season3 = Season(id=3, season='Всесезонная', look_season='Всесезонный')
    # session.add(season3)
    # season4 = Season(id=4, season='Демисезонная', look_season='Демисезонный')
    # session.add(season4)
    #
    # functionality1 = Functionality(id=1, functionality='Верхняя')
    # session.add(functionality1)
    # functionality2 = Functionality(id=2, functionality='Верхняя лёгкая')
    # session.add(functionality2)
    #
    # style1 = Style(id=1, style='Деловой')
    # session.add(style1)
    # style2 = Style(id=2, style='Казуальный')
    # session.add(style2)
    # style3 = Style(id=3, style='Спортивный')
    # session.add(style3)
    #
    # type1 = Type(id=1, type='Плечевая')
    # session.add(type1)
    # type2 = Type(id=2, type='Поясная')
    # session.add(type2)


if __name__ == '__main__':
    main()