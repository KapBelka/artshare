import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


association_table = sqlalchemy.Table("notetocategories", SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('noteid', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('notes.id')),
                                     sqlalchemy.Column('categoryid', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('categories.id'))
                                     )


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
