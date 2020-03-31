from flask_restful import reqparse, Resource, abort
from data.categories import Category, association_table as assoc_table
from flask import jsonify, g
from sqlalchemy import desc
from api_auth import token_auth
from data.notes import Note
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)

parser_for_get = reqparse.RequestParser()
parser_for_get.add_argument('start_id', type=int)
parser_for_get.add_argument('count', type=int)
parser_for_get.add_argument('category', type=int)


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
        if not args['count']:
            count = 15
        if args['category']:
            notes = session.query(Note).filter(Note.id <= start_id, assoc_table.c.noteid == Note.id,
                                               assoc_table.c.categoryid == category).order_by(
                                               Note.date.desc()).limit(count).all()
        else:
            notes = session.query(Note).filter(Note.id <= start_id).order_by(Note.date.desc()).limit(count).all()
        if not notes:
            abort(404, message=f"Notes not found")
        return jsonify(
            {
                'notes': [note.to_dict(only=('id', 'authorid', 'title', 'text')) for note in notes]
            }
        )
