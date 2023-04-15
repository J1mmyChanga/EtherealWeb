from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, RadioField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    sex = RadioField('Пол:', choices=[(1, 'Мужской'), (2, 'Женский')], validators=[DataRequired()])
    nickname = StringField('Никнейм', validators=[DataRequired()])
    image = FileField('Выберите аватар')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    nickname = StringField('Никнейм')
    image = FileField('Выберите аватар')
    submit = SubmitField('Сохранить')