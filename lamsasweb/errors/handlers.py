from flask import Blueprint, render_template
from sqlite3 import OperationalError
from werkzeug.exceptions import HTTPException

Template = str
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(401)
def error_401(error: HTTPException) -> tuple[Template, int]:
    return render_template('errors/401.html'), 401


@errors.app_errorhandler(404)
def error_404(error: HTTPException) -> tuple[Template, int]:
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error: HTTPException) -> tuple[Template, int]:
    return render_template('errors/500.html',), 500


@ errors.app_errorhandler(OperationalError)
def error_operational(error: HTTPException) -> tuple[Template, int]:
    return render_template('errors/operational.html'), 422
