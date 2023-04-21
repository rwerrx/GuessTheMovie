import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Soundtracks(SqlAlchemyBase):
    __tablename__ = 'soundtracks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    filename = sqlalchemy.Column(sqlalchemy.String, unique=True)
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('films.id'))
    film = orm.relationship('Films')
