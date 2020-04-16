from flask_restful import Resource
from flask import jsonify, g
from api_auth import auth, token_auth
import datetime
import base64
import os


def create_token():
    token = base64.b64encode(os.urandom(24)).decode('utf-8')
    return token


class TokenResource(Resource):
    @auth.login_required
    def get(self):
        exp_in = 3600
        session = g.session
        user = g.current_user
        if user.token and user.token_exp > datetime.datetime.utcnow() + datetime.timedelta(seconds=60):
            token = user.token
        else:
            token = create_token()
            user.token = token
            user.token_exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_in)
            session.add(user)
            session.commit()
        return jsonify({'token': token})

    @token_auth.login_required
    def post(self):
        return jsonify({'user': g.current_user.to_dict(only=('id', 'nickname', 'about', 'email'))})

    @token_auth.login_required
    def delete(self):
        g.current_user.token_exp = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        g.session.commit()
        return jsonify({'success': 'OK'})
