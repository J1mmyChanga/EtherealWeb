import io

from PIL import Image
from flask_restful import Api
from flask import Flask, render_template, redirect, url_for, request, abort, session
from werkzeug.serving import WSGIRequestHandler
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

from data import db_session
from data.clothes import Clothes
from data.looks import Looks
from data.users import Users
from data.custom_looks import CustomLooks

from forms.user import RegisterForm, LoginForm, EditForm
from forms.clothes import ClothesForm
from resources import *
from forms.custom_looks import CustomLooksForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(SetClothesInWardrobe, "/api/addInWardrobeResource/")
api.add_resource(GetClothesFromWardrobeResource, "/api/clothesByParams/")
api.add_resource(GetClothesInfoResource, "/api/ci/")
api.add_resource(LoginResource, "/api/login/")
api.add_resource(WardrobeResource, "/api/wardrobe/")

db_session.global_init('db/ethereal.db')


@app.route('/wardrobe')
@login_required
def wardrobe():
    param = {
        "title": "Мой гардероб",
        "outer": [],
        "top": [],
        "lower": []
    }
    session = db_session.create_session()
    clothes = session.get(Users, current_user.id).clothes
    for item in clothes:
        if item.type == 1:
            param['outer'].append(item)
        elif item.type == 2:
            param['top'].append(item)
        elif item.type == 3:
            param['lower'].append(item)
    param['path'] = url_for('static', filename='img/clothes_def')
    return render_template("wardrobe.html", **param)


@app.route('/add_clothes', methods=['GET', 'POST'])
@login_required
def add_clothes():
    form = ClothesForm()
    param = {}
    clothes = []
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.get(Users, current_user.id)
        clothes = session.query(Clothes).filter(Clothes.type == form.type.data,
                                                Clothes.season == form.season.data).all()
        selected_item_id = request.form.get('item_id')
        if selected_item_id:
            user.clothes.append(session.get(Clothes, selected_item_id))
            session.commit()
    print(clothes)
    param['title'] = 'Добавление одежды'
    param['clothes'] = clothes
    param['form'] = form
    param['path'] = url_for('static', filename='img/clothes_def')
    return render_template('add_clothes.html', **param)


@app.route('/clothes_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def clothes_delete(id):
    session = db_session.create_session()
    clothes = session.get(Clothes, id)
    user_clothes = session.get(Users, current_user.id)
    if clothes:
        user_clothes.clothes.remove(clothes)
        session.commit()
    else:
        abort(404)
    return redirect('/wardrobe')


@app.route('/looks')
@login_required
def looks():
    param = {}
    looks = []
    param['casual'] = []
    param['business'] = []
    param['sportswear'] = []
    session = db_session.create_session()
    clothes = session.get(Users, current_user.id).clothes
    for look in session.query(Looks).filter((Looks.sex == current_user.sex) | (Looks.sex == 3)):
        item_list = []
        for item in look.clothes:
            if item in clothes:
                item_list.append(item)
                continue
            else:
                break
        if len(item_list) >= 2:
            looks.append(look)
    for item in looks:
        if item.style == 1:
            param['business'].append(item)
        elif item.style == 2:
            param['casual'].append(item)
        elif item.style == 3:
            param['sportswear'].append(item)
    param['title'] = 'Мои образы'
    param['path'] = url_for('static', filename='img/clothes_def')
    return render_template("looks.html", **param)


@app.route('/')
@app.route('/looks_feed')
def looks_feed():
    param = {}
    session = db_session.create_session()
    param['custom_looks'] = []
    for item in session.query(CustomLooks).all():
        if item.style:
            param['custom_looks'].append(item)
    param['custom_looks'] = param['custom_looks'][::-1]
    param['title'] = 'Лента образов'
    param['path'] = url_for('static', filename='img/clothes_def')
    return render_template("looks_feed.html", **param)


@app.route('/create_looks', methods=['GET', 'POST'])
@login_required
def create_looks():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    session_ = db_session.create_session()
    if visits_count == 0:
        custom_look = CustomLooks(
            user=current_user.id,
            description=''
        )
    else:
        custom_look = session_.query(CustomLooks).filter(CustomLooks.user == current_user.id).all()[-1]
    form = CustomLooksForm()
    param = {'title': 'Создание образа', 'form': form, 'custom_look': custom_look, 'outer': [], 'top': [], 'lower': []}
    all_clothes = session_.query(Clothes).all()
    for item in all_clothes:
        if item.type == 1:
            param['outer'].append(item)
        elif item.type == 2:
            param['top'].append(item)
        elif item.type == 3:
            param['lower'].append(item)
    param['path'] = url_for('static', filename='img/clothes_def')
    session_.add(custom_look)
    session_.commit()
    if form.validate_on_submit():
        if len(custom_look.clothes) < 2:
            return render_template('create_looks.html', **param, message='В образе не хватает одежды')
        session['visits_count'] = 0
        custom_look.style = form.style.data
        custom_look.season = form.season.data
        custom_look.sex = form.sex.data
        custom_look.description = form.description.data
        session_.commit()
        return redirect('/looks_feed')
    return render_template('create_looks.html', **param)


@app.route('/delete_looks/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_looks(id):
    session = db_session.create_session()
    custom_look = session.query(CustomLooks).filter(CustomLooks.id == id, CustomLooks.user == current_user.id).first()
    if custom_look:
        session.delete(custom_look)
        session.commit()
    else:
        abort(404)
    return redirect('/looks_feed')


@app.route('/add_clothes_to_looks/<int:look_id>/<int:clothes_id>', methods=['GET', 'POST'])
@login_required
def add_clothes_to_looks(look_id, clothes_id):
    session = db_session.create_session()
    clothes = session.get(Clothes, clothes_id)
    custom_look = session.get(CustomLooks, look_id)
    if clothes:
        custom_look.clothes.append(clothes)
        session.commit()
    else:
        abort(404)
    return redirect('/create_looks')


@app.route('/delete_clothes_in_looks/<int:look_id>/<int:clothes_id>', methods=['GET', 'POST'])
@login_required
def delete_clothes_in_looks(look_id, clothes_id):
    session = db_session.create_session()
    clothes = session.get(Clothes, clothes_id)
    custom_look = session.get(CustomLooks, look_id)
    if clothes:
        custom_look.clothes.remove(clothes)
        session.commit()
    else:
        abort(404)
    return redirect('/create_looks')


@app.route('/favourite')
@login_required
def favourite():
    param = {}
    param['title'] = 'Избранное'
    param['casual'] = []
    param['business'] = []
    param['sportswear'] = []
    param['path'] = url_for('static', filename='img/clothes_def')
    session = db_session.create_session()
    favourites = session.get(Users, current_user.id).favourite_looks + session.get(Users,
                                                                                   current_user.id).favourite_custom_looks
    for item in favourites:
        if item.style == 1:
            param['business'].append(item)
        elif item.style == 2:
            param['casual'].append(item)
        elif item.style == 3:
            param['sportswear'].append(item)
    return render_template('favourite.html', **param)


@app.route('/add_favourite/<int:id>', methods=['GET', 'POST'])
@login_required
def add_favourite_from_looks(id):
    session = db_session.create_session()
    look = session.get(Looks, id)
    favourites = session.get(Users, current_user.id)
    if look:
        favourites.favourite_looks.append(look)
        session.commit()
    else:
        abort(404)
    return redirect(f'/looks')


@app.route('/add_favourite_custom/<int:id>', methods=['GET', 'POST'])
@login_required
def add_favourite_from_feed(id):
    session = db_session.create_session()
    look = session.get(CustomLooks, id)
    favourites = session.get(Users, current_user.id)
    if look:
        favourites.favourite_custom_looks.append(look)
        session.commit()
    else:
        abort(404)
    return redirect(f'/looks_feed')


@app.route('/delete_favourite/<string:type>/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_favourite(type, id):
    session = db_session.create_session()
    if type == 'looks':
        look = session.get(Looks, id)
        favourites = session.get(Users, current_user.id)
        if look:
            favourites.favourite_looks.remove(look)
            session.commit()
        else:
            abort(404)
    else:
        look = session.get(CustomLooks, id)
        favourites = session.get(Users, current_user.id)
        if look:
            favourites.favourite_custom_looks.remove(look)
            session.commit()
        else:
            abort(404)
    return redirect('/favourite')


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['visits_count'] = 0
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
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        if form.image.data:
            user.image = convert_to_image(convert_to_binary(form.image.data))
            db_sess.commit()
        return redirect("/")
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
            user.image = convert_to_image(convert_to_binary(form.image.data))
        if form.password.data:
            user.set_password(form.password.data)

        db_sess.commit()
        return redirect('/')
    else:
        form.nickname.data = user.nickname
        form.email.data = user.email
    return render_template('edit_profile.html', title='Личные данные', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['visits_count'] = 0
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               title='Авторизация',
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
    session['visits_count'] = 0
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(Users, user_id)


def main():
    session = db_session.create_session()
    session.commit()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
