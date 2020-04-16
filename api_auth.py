from data import db_session
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import abort
from flask import g
from data.users import User
import datetime

auth = HTTPBasicAuth()


@auth.verify_password  # подключаем проверку пароля flask-httpauth
def verify_password(email, password):
    """Сверяет email и пароль с базой данных"""
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if user:
        g.current_user = user
        g.session = session
        return (user.check_password(password))
    abort(401, error="Unauthorized")


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    """Сверяет token с базой данных"""
    session = db_session.create_session()
    user = session.query(User).filter(User.token == token).first()
    if user and user.token_exp > datetime.datetime.utcnow():
        g.current_user = user
        g.session = session
        return True
    abort(401, error="Unauthorized")
