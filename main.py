from flask import Flask, redirect, render_template, request, make_response
from flask_wtf import FlaskForm
from data import db_session
from flask_restful import abort, Api
from data.users import User
from users_api.classes import users_list_resource, users_resource
from users_api.classes import subscribe_resource, subscribe_list_resource
from notes_api.classes import notes_list_resourse, notes_resourse
from wtforms import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired
import token_resource
import requests

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'artshare_key_2013381'


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


def get_token():
    token = request.cookies.get("token")
    if token:
        return token


def validate_token(token):
    answer = requests.post('http://127.0.0.1:5000/api/token', headers={'Authorization': f'Bearer {token}'}).json()
    return 'success' in answer


@app.route("/")
def redirect_to_startpage():
    return redirect("/index")


@app.route("/index")
def startpage():
    param = {'title': 'ArtShare',
             'is_auth': validate_token(get_token())}
    return render_template('index.html', **param)


@app.route("/subscribes")
def subscribespage():
    token = get_token()
    is_token_valid = validate_token(get_token())
    if not is_token_valid:
        return redirect('/')
    subscribe_users = requests.get('http://127.0.0.1:5000/api/users/subscribe', headers={'Authorization': f'Bearer {token}'}).json()
    print(subscribe_users)
    param = {'title': 'ArtShare',
             'is_auth': is_token_valid,
             'subscribe_users': subscribe_users['users']}
    return render_template('subscribes.html', **param)


@app.route("/subscribe/<int:user_id>")
def subscribe(user_id):
    token = get_token()
    is_token_valid = validate_token(get_token())
    if not is_token_valid:
        return redirect('/')
    requests.post(f'http://127.0.0.1:5000/api/users/subscribe/{user_id}', headers={'Authorization': f'Bearer {token}'}).json()
    return redirect('/')


@app.route("/login", methods=['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        data = requests.get('http://127.0.0.1:5000/api/token', auth=(form.email.data, form.password.data)).json()
        if data:
            res = make_response(redirect("/"))
            res.set_cookie("token", data['token'], max_age=60 * 60)
            return res
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/artshare.sqlite")
    api.add_resource(token_resource.TokenResource, '/api/token')
    api.add_resource(users_list_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(subscribe_resource.SubscribeResource, '/api/users/subscribe/<int:user_id>')
    api.add_resource(subscribe_list_resource.SubscribeListResource, '/api/users/subscribe')
    api.add_resource(notes_list_resourse.NotesListResourse, '/api/notes')
    api.add_resource(notes_resourse.NotesResourse, '/api/notes/<int:note_id>')
    app.run()


if __name__ == "__main__":
    main()
