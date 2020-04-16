from flask_restful import reqparse, Resource, abort, request
from flask import jsonify, g
from data.users import User
from data import db_session
from api_auth import token_auth
from files import *

parser = reqparse.RequestParser()
parser.add_argument('password')
parser.add_argument('nickname')
parser.add_argument('about')
parser.add_argument('remove_img')


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user:
            return jsonify(user.to_dict(only=('about', 'email', 'id', 'nickname', 'photo')))
        abort(404, message=f"User {user_id} not found")

    @token_auth.login_required
    def put(self, user_id):
        session = g.session
        user = g.current_user
        if user.id == user_id:
            args = parser.parse_args()
            if args['about']:
                user.about = args['about']
            if args['nickname']:
                user.nickname = args['nickname']
            if args['password']:
                user.set_password(args['password'])
            if 'img_file' in request.files:
                img_file = request.files['img_file']
                user.photo = create_img_file(img_file, 'profiles')
            if args['remove_img'] == 'True':
                user.photo = "default.jpg"
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
