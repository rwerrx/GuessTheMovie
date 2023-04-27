import flask
from flask import jsonify

from data import db_session
from data.films import Films

blueprint = flask.Blueprint(
    'films_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/films')
def get_films():
    db_sess = db_session.create_session()
    films = db_sess.query(Films).all()
    return jsonify(
        {
            'films':
                [item.to_dict(only=('title', 'id'))
                 for item in films]
        }
    )