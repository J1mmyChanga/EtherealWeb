from flask import Flask
from data import db_session

app = Flask(__name__)

def main():
    db_session.global_init('db/ethereal.db')
    app.run()


@app.route('/')
def index():
    return 'Good luck!'

if __name__ == '__main__':
    main()