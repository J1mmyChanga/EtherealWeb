import io

from PIL import Image
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, logout_user, login_user

from data import db_session
from data.clothes import Clothes
from data.functionality import Functionality
from data.looks import Looks
from data.season import Season
from data.sex import Sex
from data.style import Style
from data.type import Type
from data.users import Users

from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    param = {}
    param['title'] = 'Главная'
    return render_template("index.html", **param)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(Users, user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = Users(
            email=form.email.data,
            sex=form.sex.data,
            nickname=form.nickname.data,
            image=convert_to_binary(form.image.data)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def convert_to_binary(img):
    image = Image.open(img)
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='JPEG')
    byte_image = byte_stream.getvalue()
    return byte_image


def main():
    db_session.global_init('db/ethereal.db')
    session = db_session.create_session()
    session.commit()
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()
