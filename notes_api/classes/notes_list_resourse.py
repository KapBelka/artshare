from flask_restful import reqparse, Resource, abort, request
from data.categories import Category
from flask import jsonify, g
from sqlalchemy import desc
from api_auth import token_auth
from data.notes import Note
from data.users import User
from data import db_session
from files import *
import uuid


parser = reqparse.RequestParser()
parser.add_argument('text')
parser.add_argument('category', required=True)
parser.add_argument('remove_img')
parser.add_argument('remove_audio')

parser_for_get = reqparse.RequestParser()
parser_for_get.add_argument('start_id', type=int)
parser_for_get.add_argument('count', type=int)
parser_for_get.add_argument('category', type=int)
parser_for_get.add_argument('subscribe', type=int)
parser_for_get.add_argument('authorid', type=int)
parser_for_get.add_argument('search')


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
            note.img_file = create_img_file(img_file, "notes")
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            note.audio_file = create_audio_file(audio_file, "notes")
        if args['remove_img'] == 'True':
            note.img_file = None
        if args['remove_audio'] == 'True':
            note.audio_file = None
        session.add(note)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        args = parser_for_get.parse_args()
        session = db_session.create_session()
        start_id = args['start_id']
        category = args['category']
        subscribe = args['subscribe']
        search = args['search']
        count = args['count']
        authorid = args['authorid']
        query = session.query(Note, User).filter(User.id == Note.authorid)
        if start_id:
            query = query.filter(Note.id <= start_id)
        if search:
            query = query.filter(Note.text.like(f'%{search}%') | User.nickname.like(f'%{search}%'))
        if authorid:
            query = query.filter(Note.authorid == authorid)
        if category:
            query = query.filter(Note.category == category)
        if subscribe:
            user = session.query(User).get(subscribe)
            query = query.filter(Note.authorid.in_(user.subscribe_users[1:-1].split(':')))
        query = query.order_by(Note.date.desc())
        if count:
            query = query.limit(count)
        notes = query.all()
        print('asd', notes)
        if not notes:
            return jsonify({'notes': []})
        return jsonify(
            {
                'notes': [{'note': note_user[0].to_dict(only=('id', 'text', 'img_file', 'audio_file')),
                           'author': note_user[1].to_dict(only=('nickname', 'id'))} for note_user in notes]
            }
        )
