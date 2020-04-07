from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.users import User, association_table as assoc_table
from data import db_session
from api_auth import auth, token_auth


class SubscribeResource(Resource):
    @token_auth.login_required
    def post(self, user_id):
        session = g.session
        user = g.current_user
        to_user = session.query(User).get(user_id)
        if to_user:
            return jsonify({'success': 'OK'})
        return abort(404, message=f"User {user_id} not found")
    
    @token_auth.login_required
    def delete(self, user_id):
        session = g.session
        user = g.current_user
        to_user = session.query(User).get(user_id)
        if to_user:
            pass
            session.commit()
            return jsonify({'success': 'OK'})
        return abort(404, message=f"User {user_id} not found")
    
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query("User").get(user_id)
        if user:
            return jsonify({"users": [usr.to_dict(only=('id', 'nickname')) for usr in user.subscript_users]})
        return abort(404, message=f"User {user_id} not found")
