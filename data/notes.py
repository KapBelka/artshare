import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Note(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'notes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    authorid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    img_file = sqlalchemy.Column(sqlalchemy.String)
    audio_file = sqlalchemy.Column(sqlalchemy.String)


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


association_table = sqlalchemy.Table("notetocategories", SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('noteid', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('notes.id')),
                                     sqlalchemy.Column('categoryid', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('categories.id'))
                                     )
