from flask import Flask
from lamsasweb.search.utils import get_downloads_folder


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change_this_later'
    app.config['DOWNLOAD_PATH'] = get_downloads_folder(__file__)
    from lamsasweb.search.routes import search
    from lamsasweb.errors.handlers import errors
    app.register_blueprint(search)
    app.register_blueprint(errors)
    return app
