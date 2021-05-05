import os
import ast
from sqlite3 import OperationalError

from flask import (Blueprint, render_template, redirect,
                   url_for, request, send_from_directory, abort, current_app)
from lamsasweb.search.forms import (DBSimpleQueryForm, DBAdvancedQueryForm,
                                    DBRawQueryForm)
from lamsasweb.search.utils import (all_columns, generate_query, query_db,
                                    make_results_zip,
                                    query_args_from_form, get_args_from_query)

Template = str
search = Blueprint('search', __name__)


@search.route('/')
@search.route('/home')
def home() -> Template:
    return render_template('home.html', title='Home')


@search.route('/help')
def help() -> Template:
    return render_template('help.html', title='Help')


@search.route('/query-simple', methods=['GET', 'POST'])
def query_simple() -> Template:
    form = DBSimpleQueryForm()
    if form.validate_on_submit():
        query_args = query_args_from_form(
            form, ('submit', 'csrf_token'))
        return redirect(url_for('search.query_results', query_args=query_args))
    return render_template('query_simple.html', form=form,
                           all_columns=all_columns, title='Query')


@search.route('/query-advanced', methods=['GET', 'POST'])
def query_advanced() -> Template:
    form = DBAdvancedQueryForm()
    if form.validate_on_submit():
        query_args = query_args_from_form(
            form, ('submit', 'csrf_token', 'show_query'))
        return redirect(url_for('search.query_results',
                                show_query=form.data['show_query'],
                                query_args=query_args))
    return render_template('query_advanced2.html', form=form,
                           all_columns=all_columns, title='Query')


@search.route('/query-raw', methods=['GET', 'POST'])
def query_raw() -> Template:
    form = DBRawQueryForm()
    if form.validate_on_submit():
        try:
            query_args = get_args_from_query(form.data['raw_query'])
        except Exception:
            raise OperationalError
        return redirect(url_for('search.query_results',
                                query_args=query_args, show_query=True))
    return render_template('query_raw.html', form=form, title='Query (RAW)')


@search.route('/query-results')
def query_results() -> Template:
    query_args = ast.literal_eval(request.args.get('query_args'))
    show_query = request.args.get('show_query')
    query = generate_query(query_args)
    results = query_db(query)
    return render_template('query_results.html', query_args=query_args,
                           results=results, query=query,
                           show_query=show_query, title='Results')


@search.route('/download-results')
def download_results() -> Template:
    query_args = ast.literal_eval(request.args.get('query_args'))
    query_results = query_db(generate_query(query_args))
    download_path = current_app.config['DOWNLOAD_PATH']
    try:
        filename = make_results_zip(download_path, query_args, query_results)
    except Exception:
        abort(500)
    else:
        try:
            return send_from_directory(download_path, filename=filename,
                                       as_attachment=True, cache_timeout=0)
        except FileNotFoundError:
            abort(404)
        else:
            os.remove(download_path + filename)
