from data import db_session
from data.clothes import Clothes
from data.looks import Looks
from data.season import Season
from data.sex import Sex
from data.style import Style
from data.type import Type
from data.users import Users


db_session.global_init('db/ethereal.db')
session = db_session.create_session()
s1 = Sex(sex='Мужской')
session.add(s1)
s2 = Sex(sex='Женский')
session.add(s2)
s3 = Sex(sex='Унисекс')
session.add(s3)

season1 = Season(id=1, season='Лето', look_season='Летний')
session.add(season1)
season2 = Season(id=2, season='Зима', look_season='Зимний')
session.add(season2)
season3 = Season(id=3, season='Всесезонная', look_season='Всесезонный')
session.add(season3)
season4 = Season(id=4, season='Демисезонная', look_season='Демисезонный')
session.add(season4)

style1 = Style(id=1, style='Деловой')
session.add(style1)
style2 = Style(id=2, style='Свободный')
session.add(style2)
style3 = Style(id=3, style='Спортивный')
session.add(style3)

type1 = Type(id=1, type='Верхняя')
session.add(type1)
type2 = Type(id=2, type='Верхняя лёгкая')
session.add(type2)
type3 = Type(id=3, type='Поясная')
session.add(type3)

c1 = Clothes(id=1, name='Пальто', type=1, season=4)
c2 = Clothes(id=2, name='Пуховик', type=1, season=2)
c3 = Clothes(id=3, name='Плащ', type=1, season=4)
c4 = Clothes(id=4, name='Бомбер', type=1, season=4)
c5 = Clothes(id=5, name='Ветровка', type=1, season=1)
c6 = Clothes(id=6, name='Косуха', type=1, season=4)
c7 = Clothes(id=7, name='Парка', type=1, season=4)
c8 = Clothes(id=8, name='Блуза', type=2, season=3)
c9 = Clothes(id=9, name='Классические брюки', type=3, season=4)
c10 = Clothes(id=10, name='Джемпер', type=2, season=4)
c11 = Clothes(id=11, name='Жилет', type=2, season=3)
c12 = Clothes(id=12, name='Кардиган', type=2, season=4)
c13 = Clothes(id=13, name='Кофта', type=2, season=2)
c14 = Clothes(id=14, name='Пиджак', type=2, season=4)
c15 = Clothes(id=15, name='Рубашка', type=2, season=3)
c16 = Clothes(id=16, name='Свитер', type=2, season=2)
c17 = Clothes(id=17, name='Шорты', type=3, season=1)
c18 = Clothes(id=18, name='Юбка', type=3, season=1)
c19 = Clothes(id=19, name='Майка', type=2, season=1)
c20 = Clothes(id=20, name='Футболка', type=2, season=1)
c21 = Clothes(id=21, name='Водолазка', type=2, season=3)
c22 = Clothes(id=22, name='Пуловер', type=2, season=4)
c23 = Clothes(id=23, name='Милитари', type=3, season=4)
c24 = Clothes(id=24, name='Джинсы', type=3, season=3)
c25 = Clothes(id=25, name='Лыжная куртка', type=1, season=2)
c26 = Clothes(id=26, name='Бушлат', type=1, season=2)
c27 = Clothes(id=27, name='Стеганая куртка', type=1, season=2)
c28 = Clothes(id=28, name='Комбинезон', type=3, season=2)
c29 = Clothes(id=29, name='Джоггеры', type=3, season=4)
c30 = Clothes(id=30, name='Карго', type=3, season=4)
c31 = Clothes(id=31, name='Спортивные штаны', type=3, season=1)
c32 = Clothes(id=32, name='Джинсовка', type=1, season=1)
c33 = Clothes(id=33, name='Кожаная куртка', type=1, season=4)
c34 = Clothes(id=34, name='Дублёнка', type=1, season=2)
c35 = Clothes(id=35, name='Рубашка(короткий рукав)', type=2, season=1)
c36 = Clothes(id=36, name='Брюки', type=3, season=4)
c37 = Clothes(id=37, name='Джинсы(утеплённые)', type=3, season=2)
for i in range(1, 38):
    eval(f'c{i}').image = f"{i}.png"
    session.add(eval(f'c{i}'))

l1 = Looks(id=1, style=2, season=1, sex=3)
l2 = Looks(id=2, style=2, season=1, sex=3)
l3 = Looks(id=3, style=2, season=1, sex=2)
l4 = Looks(id=4, style=2, season=1, sex=3)
l5 = Looks(id=5, style=1, season=1, sex=3)
l6 = Looks(id=6, style=3, season=1, sex=1)
l7 = Looks(id=7, style=1, season=1, sex=1)
l8 = Looks(id=8, style=2, season=1, sex=3)
l9 = Looks(id=9, style=2, season=1, sex=2)
l10 = Looks(id=10, style=3, season=1, sex=1)
l11 = Looks(id=11, style=3, season=1, sex=1)
l12 = Looks(id=12, style=2, season=2, sex=3)
l13 = Looks(id=13, style=2, season=2, sex=1)
l14 = Looks(id=14, style=2, season=2, sex=1)
l15 = Looks(id=15, style=2, season=2, sex=1)
l16 = Looks(id=16, style=1, season=2, sex=3)
l17 = Looks(id=17, style=2, season=2, sex=3)
l18 = Looks(id=18, style=1, season=2, sex=1)
l19 = Looks(id=19, style=2, season=2, sex=1)
l20 = Looks(id=20, style=3, season=2, sex=3)
l21 = Looks(id=21, style=1, season=4, sex=3)
l22 = Looks(id=22, style=3, season=4, sex=3)
l23 = Looks(id=23, style=2, season=4, sex=3)
l24 = Looks(id=24, style=2, season=4, sex=1)
l25 = Looks(id=25, style=2, season=4, sex=1)
l26 = Looks(id=26, style=2, season=4, sex=1)
l27 = Looks(id=27, style=2, season=4, sex=3)
l28 = Looks(id=28, style=1, season=4, sex=1)
for i in range(1, 29):
    session.add(eval(f'l{i}'))

l1.clothes.append(session.get(Clothes, 32))
l1.clothes.append(session.get(Clothes, 20))
l1.clothes.append(session.get(Clothes, 36))

l2.clothes.append(session.get(Clothes, 20))
l2.clothes.append(session.get(Clothes, 17))

l3.clothes.append(session.get(Clothes, 15))
l3.clothes.append(session.get(Clothes, 20))

l4.clothes.append(session.get(Clothes, 20))
l4.clothes.append(session.get(Clothes, 36))

l5.clothes.append(session.get(Clothes, 15))
l5.clothes.append(session.get(Clothes, 9))

l6.clothes.append(session.get(Clothes, 20))
l6.clothes.append(session.get(Clothes, 29))

l7.clothes.append(session.get(Clothes, 35))
l7.clothes.append(session.get(Clothes, 36))

l8.clothes.append(session.get(Clothes, 35))
l8.clothes.append(session.get(Clothes, 17))

l9.clothes.append(session.get(Clothes, 8))
l9.clothes.append(session.get(Clothes, 24))

l10.clothes.append(session.get(Clothes, 20))
l10.clothes.append(session.get(Clothes, 31))

l11.clothes.append(session.get(Clothes, 5))
l11.clothes.append(session.get(Clothes, 19))
l11.clothes.append(session.get(Clothes, 31))

l12.clothes.append(session.get(Clothes, 2))
l12.clothes.append(session.get(Clothes, 16))
l12.clothes.append(session.get(Clothes, 37))

l13.clothes.append(session.get(Clothes, 2))
l13.clothes.append(session.get(Clothes, 13))
l13.clothes.append(session.get(Clothes, 30))

l14.clothes.append(session.get(Clothes, 26))
l14.clothes.append(session.get(Clothes, 21))
l14.clothes.append(session.get(Clothes, 36))

l15.clothes.append(session.get(Clothes, 26))
l15.clothes.append(session.get(Clothes, 11))
l15.clothes.append(session.get(Clothes, 37))

l16.clothes.append(session.get(Clothes, 27))
l16.clothes.append(session.get(Clothes, 10))
l16.clothes.append(session.get(Clothes, 36))

l17.clothes.append(session.get(Clothes, 27))
l17.clothes.append(session.get(Clothes, 21))
l17.clothes.append(session.get(Clothes, 37))

l18.clothes.append(session.get(Clothes, 34))
l18.clothes.append(session.get(Clothes, 14))
l18.clothes.append(session.get(Clothes, 9))

l19.clothes.append(session.get(Clothes, 34))
l19.clothes.append(session.get(Clothes, 22))
l19.clothes.append(session.get(Clothes, 30))

l20.clothes.append(session.get(Clothes, 25))
l20.clothes.append(session.get(Clothes, 16))
l20.clothes.append(session.get(Clothes, 28))

l21.clothes.append(session.get(Clothes, 1))
l21.clothes.append(session.get(Clothes, 14))
l21.clothes.append(session.get(Clothes, 9))

l22.clothes.append(session.get(Clothes, 5))
l22.clothes.append(session.get(Clothes, 20))
l22.clothes.append(session.get(Clothes, 31))

l23.clothes.append(session.get(Clothes, 3))
l23.clothes.append(session.get(Clothes, 22))
l23.clothes.append(session.get(Clothes, 24))

l24.clothes.append(session.get(Clothes, 6))
l24.clothes.append(session.get(Clothes, 8))
l24.clothes.append(session.get(Clothes, 18))

l25.clothes.append(session.get(Clothes, 4))
l25.clothes.append(session.get(Clothes, 15))
l25.clothes.append(session.get(Clothes, 36))

l26.clothes.append(session.get(Clothes, 4))
l26.clothes.append(session.get(Clothes, 10))
l26.clothes.append(session.get(Clothes, 30))

l27.clothes.append(session.get(Clothes, 6))
l27.clothes.append(session.get(Clothes, 20))
l27.clothes.append(session.get(Clothes, 29))

l28.clothes.append(session.get(Clothes, 33))
l28.clothes.append(session.get(Clothes, 21))
l28.clothes.append(session.get(Clothes, 36))
session.commit()