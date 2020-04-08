from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.notes import Note
from data import db_session
from api_auth import token_auth
from notes_list_resourse import create_audio_file, create_img_file

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('text')


class NotesResourse(Resource):
    def get(self, note_id):
        session = db_session.create_session()
        user = session.query(Note).get(note_id)
        if user:
            return jsonify(user.to_dict(only=('authorid', 'title', 'text')))
        abort(404, message=f"User {note_id} not found")

    @token_auth.login_required
    def put(self, note_id):
        session = g.session
        user = g.current_user
        note = session.query(Note).get(note_id)
        if note.authorid == user.id:
            args = parser.parse_args()
            if 'title' in args:
                note.title = args['title']
            if 'text' in args:
                note.text = args['text']
            if 'img_file' in request.files:
                img_file = request.files['img_file']
                note.img_file = create_img_file(img_file)
            if 'audio_file' in request.files:
                audio_file = request.files['audio_file']
                note.audio_file = create_audio_file(audio_file)
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
