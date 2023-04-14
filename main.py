from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, logout_user

from data import db_session
from data.clothes import Clothes
from data.functionality import Functionality
from data.looks import Looks
from data.season import Season
from data.style import Style
from data.type import Type
from data.users import Users

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

def main():
    db_session.global_init('db/ethereal.db')
    session = db_session.create_session()
    session.commit()
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()
