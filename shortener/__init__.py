import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('SQLALCHEMY_DATABASE_URI')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
        os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    )

    db.init_app(app)

    with app.app_context():
        from .api import UrlApi

        url_view = UrlApi.as_view('url_api')
        app.add_url_rule('/api/', defaults={'enc_url': None},
                         view_func=url_view, methods=['GET'])
        app.add_url_rule('/api/', view_func=url_view, methods=['POST'])
        app.add_url_rule('/api/<string:enc_url>', view_func=url_view,
                         methods=['DELETE'])
        app.add_url_rule('/<string:enc_url>', view_func=url_view,
                         methods=['GET'])

        db.create_all()

    return app
