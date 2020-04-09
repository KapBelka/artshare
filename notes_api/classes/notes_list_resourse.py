from flask_restful import reqparse, Resource, abort, request
from data.categories import Category
from flask import jsonify, g
from sqlalchemy import desc
from api_auth import token_auth
from data.notes import Note
from data.users import User
from data import db_session
import uuid


parser = reqparse.RequestParser()
parser.add_argument('text', required=True)
parser.add_argument('category', required=True)

parser_for_get = reqparse.RequestParser()
parser_for_get.add_argument('start_id', type=int)
parser_for_get.add_argument('count', type=int, default=15)
parser_for_get.add_argument('category', type=int)
parser_for_get.add_argument('subscribe', type=int)


def create_img_file(img_file):
    if img_file.filename.endswith('.jpg'):
        img_file_name = f"{uuid.uuid4()}.jpg"
        img_file.save(f"static/img/notes/{img_file_name}")
    elif img_file.filename.endswith('.png'):
        img_file_name = f"{uuid.uuid4()}.png"
        img_file.save(f"static/img/notes/{img_file_name}")
    else:
        abort(400, message=f"File type {img_file.filename} not allowed")
    return img_file_name


def create_audio_file(audio_file):
    if audio_file.filename.endswith('.mp3'):
        audio_file_name = f"{uuid.uuid4()}.mp3"
        audio_file.save(f"static/audio/notes/{audio_file_name}")
    else:
        abort(400, message=f"File type {audio_file.filename} not allowed")
    return audio_file_name


class NotesListResourse(Resource):
    @token_auth.login_required
    def post(self):
        args = parser.parse_args()
        session = g.session
        if not session.query(Category).get(args['category']):
            abort(404, message=f"Category not found")
        note = Note(
            text=args['text'],
            category=args['category'],
            authorid=g.current_user.id
        )
        if 'img_file' in request.files:
            img_file = request.files['img_file']
            note.img_file = create_img_file(img_file)
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            note.audio_file = create_audio_file(audio_file)
        session.add(note)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        args = parser_for_get.parse_args()
        session = db_session.create_session()
        start_id = args['start_id']
        category = args['category']
        subscribe = args['subscribe']
        count = args['count']
        if not start_id:
            start_id = session.query(Note).order_by(Note.id.desc()).first().id
        query = session.query(Note, User).filter(Note.id <= start_id, User.id == Note.authorid)
        if category:
            query = query.filter(Note.category == category)
        if subscribe:
            user = session.query(User).get(subscribe)
            query = query.filter(Note.authorid.in_(user.subscribe_users[1:-1].split(':')))
        notes = query.order_by(Note.date.desc()).limit(count).all()
        if not notes:
            abort(404, message=f"Notes not found")
        return jsonify(
            {
                'notes': [{'note': note_user[0].to_dict(only=('id', 'text', 'img_file', 'audio_file')),
                           'author': note_user[1].to_dict(only=('nickname', 'id'))} for note_user in notes]
            }
        )
