from flask_restful import reqparse, Resource, abort
from flask import jsonify, g
from data.notes import Note
from data import db_session
from api_auth import token_auth

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('text')
parser.add_argument('authorid')


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
        note = g.current_note
        if note.id == note_id:
            args = parser.parse_args()
            if 'authorid' in args:
                note.authorid = args['authorid']
            if 'title' in args:
                note.title = args['title']
            if 'text' in args:
                note.text = args['text']
            session.add(note)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")

    @token_auth.login_required
    def delete(self, note_id):
        session = g.session
        note = g.current_note
        if note.id == note_id:
            session.delete(note)
            session.commit()
            return jsonify({'success': 'OK'})
        abort(403, error="Forbidden")
