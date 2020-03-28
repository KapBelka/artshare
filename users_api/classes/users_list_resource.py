from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.users import User
from data import db_session
from api_auth import auth, token_auth


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('nickname', required=True)
parser.add_argument('about', required=True)


class UsersListResource(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args['email']).first()
        if user:
            abort(400, message='This email do exist')
        user = User(
            email=args['email'],
            nickname=args['nickname'],
            about=args['about'],
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})