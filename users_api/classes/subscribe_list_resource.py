from flask_restful import Resource
from flask import jsonify, g
from data.users import User
from api_auth import token_auth


class SubscribeListResource(Resource):
    @token_auth.login_required
    def get(self):
        user = g.current_user
        session = g.session
        users = session.query(User).filter(User.id.in_(user.subscribe_users[1:-1].split(':'))).order_by(
            User.id.desc()).all()
        return jsonify({"users": [usr.to_dict(only=('id', 'nickname')) for usr in users]})
