from flask_restful import reqparse, Resource, abort, request
from data.categories import Category
from flask import jsonify, g
from data.notes import Note
from data import db_session
from api_auth import token_auth
from files import *

parser = reqparse.RequestParser()
parser.add_argument('text')
parser.add_argument('category')
parser.add_argument('remove_img')
parser.add_argument('remove_audio')


class NotesResourse(Resource):
    def get(self, note_id):
        session = db_session.create_session()
        note = session.query(Note).get(note_id)
        if note:
            return jsonify(note.to_dict(only=('authorid', 'text', 'category')))
        abort(404, message=f"User {note_id} not found")

    @token_auth.login_required
    def put(self, note_id):
        session = g.session
        user = g.current_user
        note = session.query(Note).get(note_id)
        if note.authorid == user.id:
            args = parser.parse_args()
            print(args)
            if args['text']:
                note.text = args['text']
            if args['category']:
                if not session.query(Category).get(args['category']):
                    abort(404, message=f"Category not found")
                note.category = args['category']
            if 'img_file' in request.files:
                img_file = request.files['img_file']
                note.img_file = create_img_file(img_file, 'notes')
            if 'audio_file' in request.files:
                audio_file = request.files['audio_file']
                note.audio_file = create_audio_file(audio_file, 'notes')
            if args['remove_img'] == 'True':
                note.img_file = None
            if args['remove_audio'] == 'True':
                note.audio_file = None
            print(note.img_file)
            session.add(note)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")

    @token_auth.login_required
    def delete(self, note_id):
        session = g.session
        user = g.current_user
        note = session.query(Note).get(note_id)
        if note.authorid == user.id:
            session.delete(note)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")
