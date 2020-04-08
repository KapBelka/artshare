import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase, create_session, orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    token = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    token_exp = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subscribe_users = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    notes = orm.relation("Note", back_populates='user')

    def add_subscribe(self, user_id):
        if f':{user_id}:' not in self.subscribe_users:
            if len(self.subscribe_users):
                self.subscribe_users += f'{user_id}:'
            else:
                self.subscribe_users = f':{user_id}:'

    def remove_subscribe(self, user_id):
        self.subscribe_users = self.subscribe_users.replace(f':{user_id}:', ':')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)