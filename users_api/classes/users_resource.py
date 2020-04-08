from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.users import User
from data import db_session
from api_auth import auth, token_auth


parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('nickname')
parser.add_argument('about')


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user:
            return jsonify(user.to_dict(only=('about', 'email', 'id', 'nickname')))
        abort(404, message=f"User {user_id} not found")

    @token_auth.login_required
    def put(self, user_id):
        session = g.session
        user = g.current_user
        if user.id == user_id:
            args = parser.parse_args()
            if 'about' in args:
                user.about = args['about']
            if 'email' in args:
                user.email = args['email']
            if 'nickname' in args:
                user.nickname = args['nickname']
            if 'password' in args:
                user.set_password(args['password'])
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")

    @token_auth.login_required
    def delete(self, user_id):
        session = g.session
        user = g.current_user
        if user.id == user_id:
            session.delete(user)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")
    