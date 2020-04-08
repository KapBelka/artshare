from flask_restful import reqparse, Resource, abort, request
from data.categories import Category, association_table as assoc_table
from flask import jsonify, g
from sqlalchemy import desc
from api_auth import token_auth
from data.notes import Note
from data.users import User
from data import db_session
import uuid


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)

parser_for_get = reqparse.RequestParser()
parser_for_get.add_argument('start_id', type=int)
parser_for_get.add_argument('count', type=int, default=15)
parser_for_get.add_argument('category', type=int)


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
        note = Note(
            title=args['title'],
            text=args['text'],
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
        count = args['count']
        category = args['category']
        if not args['start_id']:
            start_id = session.query(Note).order_by(Note.id.desc()).first().id
        if args['category']:
            notes = session.query(Note, User).filter(Note.id <= start_id,
                            assoc_table.c.noteid == Note.id, assoc_table.c.categoryid == category,
                            User.id == Note.authorid).order_by(Note.date.desc()).limit(count).all()
        else:
            notes = session.query(Note, User).filter(Note.id <= start_id,
                            User.id == Note.authorid).order_by(Note.date.desc()).limit(count).all()
        if not notes:
            abort(404, message=f"Notes not found")
        return jsonify(
            {
                'notes': [{'note': note_user[0].to_dict(only=('id', 'title', 'text', 'img_file', 'audio_file')),
                           'author': note_user[1].to_dict(only=('nickname', 'id'))} for note_user in notes]
            }
        )
