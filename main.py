import io

from PIL import Image
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

from data import db_session
from data.clothes import Clothes
from data.functionality import Functionality
from data.looks import Looks
from data.season import Season
from data.sex import Sex
from data.style import Style
from data.type import Type
from data.users import Users

from forms.user import RegisterForm, LoginForm, EditForm
from forms.clothes import ClothesForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    param = {}
    param['title'] = 'Главная'
    session = db_session.create_session()
    return render_template("index.html", **param)


@app.route('/wardrobe', methods=['GET', 'POST'])
@login_required
def wardrobe():
    param = {}
    param['title'] = 'Мой гардероб'
    session = db_session.create_session()
    clothes = session.query(Users).get(current_user.id).clothes
    path = url_for('static', filename='img/clothes_def')
    return render_template("wardrobe.html", **param, clothes=clothes, path=path)


@app.route('/add_clothes', methods=['GET', 'POST'])
@login_required
def add_clothes():
    form = ClothesForm()
    clothes = []
    path = url_for('static', filename='img/clothes_def')
    selected_item_id = None
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.get(Users, current_user.id)
        clothes = session.query(Clothes).filter(Clothes.type == form.type.data,
                                                Clothes.func == form.functionality.data,
                                                Clothes.season == form.season.data).all()
        selected_item_id = request.form.get('item_id')
        if selected_item_id:
            user.clothes.append(session.get(Clothes, selected_item_id))
            session.commit()
    return render_template('add_clothes.html', title='Добавление одежды', form=form, clothes=clothes, path=path, selected_item_id=selected_item_id)


@app.route('/looks', methods=['GET', 'POST'])
def looks():
    param = {}
    param['title'] = 'Мои образы'
    session = db_session.create_session()
    clothes = session.query(Users).get(current_user.id).clothes
    path = url_for('static', filename='img/clothes_def')
    return render_template("wardrobe.html", **param, clothes=clothes, path=path)


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
            nickname=form.nickname.data
        )
        if form.image.data:
            user.image = convert_to_binary(form.image.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    db_sess = db_session.create_session()
    user = db_sess.get(Users, current_user.id)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit_profile.html', title='Личные данные',
                                   form=form,
                                   message="Пароли не совпадают")
        if form.nickname.data:
            user.nickname = form.nickname.data
        if form.image.data:
            user.image = convert_to_binary(form.image.data)
        if form.password.data:
            user.set_password(form.password.data)

        db_sess.commit()
        return redirect('/')
    else:
        form.nickname.data = user.nickname
        form.email.data = user.email
        if user.image:
            path_to_img = convert_to_image(user.image)
        else:
            path_to_img = ''
    return render_template('edit_profile.html', title='Личные данные', form=form, img=path_to_img)


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
    image.save(byte_stream, format=F'PNG')
    byte_image = byte_stream.getvalue()
    return byte_image


def convert_to_image(bytes_array):
    img = Image.open(io.BytesIO(bytes_array))
    img.save(url_for('static', filename=f'img/avatars/image{current_user.id}.png')[1:])
    return f"{url_for('static', filename=f'img/avatars/image{current_user.id}.png')}"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(Users, user_id)

def main():
    db_session.global_init('db/ethereal.db')
    session = db_session.create_session()
    session.commit()
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()
