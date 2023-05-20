from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length


class CustomLooksForm(FlaskForm):
    style = RadioField('Стиль:', choices=[(1, 'Деловой'), (2, 'Свободный'), (3, 'Спортивный')],
                       validators=[DataRequired()])
    season = RadioField('Сезон:', choices=[(1, 'Летний'), (2, 'Зимний'), (3, 'Демисезонный')],
                        validators=[DataRequired()])
    sex = RadioField('Пол:', choices=[(1, 'Мужской'), (2, 'Женский'), (3, 'Унисекс')], validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Length(max=200)])
    add = SubmitField('Создать')
