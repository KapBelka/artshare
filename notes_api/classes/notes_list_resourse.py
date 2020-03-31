from flask_restful import reqparse, Resource, abort
from flask import jsonify
from data.notes import Note
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)
parser.add_argument('authorid', required=True, type=int)
parser.add_argument('start_id')
parser.add_argument('count')


class NotesListResourse(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        note = Note(
            title=args['title'],
            text=args['text'],
            authorid=args['authorid']
        )
        session.add(note)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        query = session.query(Note)
        notes = query.all()
        print(notes)
        if not notes:
            abort(404, message=f"Notes not found")
        return jsonify(
            {
                'notes': notes.to_dict(only=('authorid', 'title', 'text'))
            }
        )
