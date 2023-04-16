from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class ClothesForm(FlaskForm):
    type = RadioField('Тип:', choices=[(1, 'Плечевая'), (2, 'Поясная')], validators=[DataRequired()])
    functionality = RadioField('Функциональность:', choices=[(1, 'Верхняя'), (2, 'Верхняя лёгкая')], validators=[DataRequired()])
    season = RadioField('Сезон:', choices=[(1, 'Лето'), (2, 'Зима'), (3, 'Всесезонная'), (4, 'Демисезонная')], validators=[DataRequired()])
    find = SubmitField('Найти')
    add = SubmitField('Добавить')
    