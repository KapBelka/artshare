from flask import Flask
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'artshare_key_2013381'


def main():
    db_session.global_init("db/artshare.sqlite")
    app.run()


if __name__ == "__main__":
    main()