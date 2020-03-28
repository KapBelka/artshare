from flask import Flask
from data import db_session
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort, Api
from data.users import User
from users_api.classes import users_list_resource, users_resource
import token_resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'artshare_key_2013381'


def main():
    db_session.global_init("db/artshare.sqlite")
    api.add_resource(token_resource.TokenResource, '/api/token')
    api.add_resource(users_list_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    app.run()


if __name__ == "__main__":
    main()