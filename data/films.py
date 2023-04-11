
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)

