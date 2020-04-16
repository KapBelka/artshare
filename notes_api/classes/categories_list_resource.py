from flask_restful import reqparse, Resource
from data.categories import Category
from flask import jsonify
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)


class CategoriesListResource(Resource):
    def post(self):
        session = db_session.create_session()
        args = parser.parse_args()
        category = Category(name=args['name'])
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({'categories': [elem.to_dict() for elem in categories]})
