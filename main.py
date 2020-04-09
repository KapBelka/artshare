from flask import Flask, redirect, render_template, request, make_response
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from data import db_session
from flask_restful import abort, Api
from data.users import User
from users_api.classes import users_list_resource, users_resource
from users_api.classes import subscribe_resource, subscribe_list_resource
from notes_api.classes import notes_list_resourse, notes_resourse
from notes_api.classes import categories_list_resource
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
import token_resource
import requests
import random

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'artshare_key_2013381'


API_SERVER = 'http://127.0.0.1:5000'


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class NoteForm(FlaskForm):
    text = TextField('Текст', validators=[DataRequired()])
    category = SelectField('Категория', coerce=int)
    img_file = FileField('Изображение', validators=[FileAllowed(['jpg', 'png'])])
    audio_file = FileField('Аудиозапись', validators=[FileAllowed(['mp3'])])
    submit = SubmitField('Закончить')


def get_token():
    token = request.cookies.get("token")
    if token:
        return token


def validate_token(token):
    answer = requests.post(f'{API_SERVER}/api/token', headers={'Authorization': f'Bearer {token}'})
    if answer:
        return answer.json()
    return False


@app.after_request
def off_cache(res):
    res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    res.headers["Pragma"] = "no-cache"
    res.headers["Expires"] = "0"
    res.headers['Cache-Control'] = 'public, max-age=0'
    return res


@app.route("/")
def redirect_to_startpage():
    return redirect('/index')


@app.route("/index")
def startpage():
    json_categories = requests.get(f'{API_SERVER}/api/notes/category').json()
    categories = [{"id": "null", "name": '--Все--'}]
    categories.extend(json_categories['categories'])
    user = validate_token(get_token())
    param = {'title': 'ArtShare',
             'is_auth': False,
             'categories': categories}
    if user:
        param['is_auth'] = True
        param['user'] = user['user']
    return render_template('index.html', **param)


@app.route("/subscribes")
def subscribespage():
    token = get_token()
    user = validate_token(get_token())
    if not user:
        return redirect('/')
    subscribe_users = requests.get(f'{API_SERVER}/api/users/subscribe', headers={'Authorization': f'Bearer {token}'}).json()
    param = {'title': 'ArtShare',
             'is_auth': True,
             'subscribe_users': subscribe_users['users'],
             'user': user['user']}
    return render_template('subscribes.html', **param)


@app.route("/subscribe/<int:user_id>")
def subscribe(user_id):
    token = get_token()
    is_token_valid = validate_token(get_token())
    if not is_token_valid:
        return redirect('/')
    requests.post(f'{API_SERVER}/api/users/subscribe/{user_id}', headers={'Authorization': f'Bearer {token}'}).json()
    return redirect('/')


@app.route("/unsubscribe/<int:user_id>")
def unsubscribe(user_id):
    token = get_token()
    is_token_valid = validate_token(get_token())
    if not is_token_valid:
        return redirect('/subscribes')
    requests.delete(f'{API_SERVER}/api/users/subscribe/{user_id}', headers={'Authorization': f'Bearer {token}'}).json()
    return redirect('/subscribes')


@app.route("/add_note", methods=['GET', 'POST'])
def add_notepage():
    token = get_token()
    user = validate_token(get_token())
    if not user:
        return redirect('/')
    param = {'title': 'Создание записи',
             'is_auth': True,
             'user': user['user']}
    form = NoteForm()
    categories = requests.get(f'{API_SERVER}/api/notes/category').json()
    form.category.choices = [(category['id'], category['name']) for category in categories['categories']]
    if form.validate_on_submit():
        data = {
            'text': form.text.data,
            'category': form.category.data}
        files = {}
        if form.data["img_file"]:
            files["img_file"] = (form.data["img_file"].filename, form.data["img_file"].read(), form.data["img_file"].content_type)
        if form.data["audio_file"]:
            files["audio_file"] = (form.data["audio_file"].filename, form.data["audio_file"].read(), form.data["audio_file"].content_type)
        requests.post(f'{API_SERVER}/api/notes', headers={'Authorization': f'Bearer {token}'}, data=data, files=files)
        return redirect('/')
    return render_template('note.html', form=form, **param)


@app.route("/edit_note/<int:note_id>", methods=['GET', 'POST'])
def edit_note(note_id):
    token = get_token()
    user = validate_token(get_token())
    if not user:
        return redirect('/')
    param = {'title': 'Создание записи',
             'is_auth': True,
             'user': user['user']}
    form = NoteForm()
    note = requests.get(f'{API_SERVER}/api/notes/{note_id}').json()
    categories = requests.get(f'{API_SERVER}/api/notes/category').json()
    form.category.choices = [(category['id'], category['name']) for category in categories['categories']]
    if form.validate_on_submit():
        data = {
            'text': form.text.data,
            'category': form.category.data}
        files = {}
        if form.data["img_file"]:
            files["img_file"] = (form.data["img_file"].filename, form.data["img_file"].read(), form.data["img_file"].content_type)
        if form.data["audio_file"]:
            files["audio_file"] = (form.data["audio_file"].filename, form.data["audio_file"].read(), form.data["audio_file"].content_type)
        requests.put(f'{API_SERVER}/api/notes/{note_id}', headers={'Authorization': f'Bearer {token}'}, data=data, files=files)
        return redirect('/')
    form.text.data = note['text']
    form.category.data = note['category']
    return render_template('note.html', form=form, **param)


@app.route("/delete_note/<int:note_id>")
def delete_notepage(note_id):
    token = get_token()
    is_token_valid = validate_token(get_token())
    if is_token_valid:
        requests.delete(f'{API_SERVER}/api/notes/{note_id}', headers={'Authorization': f'Bearer {token}'})
    return redirect('/')
    

@app.route("/login", methods=['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        data = requests.get(f'{API_SERVER}/api/token', auth=(form.email.data, form.password.data)).json()
        if data:
            res = make_response(redirect("/"))
            res.set_cookie("token", data['token'], max_age=60 * 60)
            return res
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout")
def logoutpage():
    token = get_token()
    is_token_valid = validate_token(get_token())
    res = make_response(redirect("/"))
    if is_token_valid:
        res.set_cookie("token", '', max_age=0)
    return res


def init_api():
    api.add_resource(token_resource.TokenResource, '/api/token')
    api.add_resource(users_list_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(subscribe_resource.SubscribeResource, '/api/users/subscribe/<int:user_id>')
    api.add_resource(subscribe_list_resource.SubscribeListResource, '/api/users/subscribe')
    api.add_resource(notes_list_resourse.NotesListResourse, '/api/notes')
    api.add_resource(notes_resourse.NotesResourse, '/api/notes/<int:note_id>')
    api.add_resource(categories_list_resource.CategoriesListResource, '/api/notes/category')


def main():
    db_session.global_init("db/artshare.sqlite")
    init_api()
    app.run()


if __name__ == "__main__":
    main()
