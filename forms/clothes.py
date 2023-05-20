from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class ClothesForm(FlaskForm):
    type = RadioField('Тип:', choices=[(1, 'Верхняя'), (2, 'Верхняя лёгкая'), (3, 'Поясная')],
                      validators=[DataRequired()])
    season = RadioField('Сезон:', choices=[(1, 'Лето'), (2, 'Зима'), (3, 'Демисезонная')], validators=[DataRequired()])
    find = SubmitField('Найти')
    add = SubmitField('Добавить')
