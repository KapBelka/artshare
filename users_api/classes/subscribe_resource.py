from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.users import User
from data import db_session
from api_auth import auth, token_auth


class SubscribeResource(Resource):
    @token_auth.login_required
    def post(self, user_id):
        session = g.session
        user = g.current_user
        to_user = session.query(User).get(user_id)
        if to_user and user.id != to_user.id:
            user.add_subscribe(user_id)
            session.commit()
            return jsonify({'success': 'OK'})
        return abort(404, message=f"User {user_id} not found")
    
    @token_auth.login_required
    def delete(self, user_id):
        session = g.session
        user = g.current_user
        to_user = session.query(User).get(user_id)
        if to_user:
            user.remove_subscribe(user_id)
            session.commit()
            return jsonify({'success': 'OK'})
        return abort(404, message=f"User {user_id} not found")
    
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user:
            users = session.query(User).filter(User.id.in_(user.subscribe_users[1:-1].split(':'))).order_by(User.id.desc()).all()
            return jsonify({"users": [usr.to_dict(only=('id', 'nickname')) for usr in users]})
        return abort(404, message=f"User {user_id} not found")
