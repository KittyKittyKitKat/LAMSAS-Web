import os
import ast
from sqlite3 import OperationalError

from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, abort, current_app, flash

from lamsasweb.search.forms import DBSimpleQueryForm, DBAdvancedQueryForm, DBRawQueryForm
from lamsasweb.search.utils import generate_query, query_db, make_results_zip, query_args_from_form, get_args_from_query

search = Blueprint('search', __name__)


@search.route('/')
@search.route('/home')
def home():
    return render_template('home.html', title='Home')


@search.route('/help')
def help():
    return render_template('help.html', title='Help')


@search.route('/query-simple', methods=['GET', 'POST'])
def query_simple():
    form = DBSimpleQueryForm()
    if request.method == 'POST':
        if form.validate():
            query_args = query_args_from_form(
                form, ('submit', 'csrf_token'))
            return redirect(url_for('search.query_results', query_args=query_args))
        else:
            for field_name, field_errors in form.errors.items():
                for error in field_errors:
                    field_label = form[field_name].label.text
                    flash(f'Error! {field_label}: {error}', 'alert alert-danger')
    return render_template('query_simple.html', form=form, title='Query')


@search.route('/query-advanced', methods=['GET', 'POST'])
def query_advanced():
    form = DBAdvancedQueryForm()
    if request.method == 'POST':
        if form.validate():
            query_args = query_args_from_form(
                form, ('submit', 'csrf_token', 'show_query'))
            return redirect(url_for('search.query_results',
                                show_query=form.data['show_query'],
                                query_args=query_args))
        else:
            for field_name, field_errors in form.errors.items():
                for error in field_errors:
                    field_label = form[field_name].label.text
                    flash(f'Error! {field_label}: {error}', 'alert alert-danger')
    return render_template('query_advanced.html', form=form, title='Query')


@search.route('/query-raw', methods=['GET', 'POST'])
def query_raw():
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
def query_results():
    query_args = ast.literal_eval(request.args.get('query_args'))
    show_query = request.args.get('show_query')
    query = generate_query(query_args)
    results = query_db(query)
    return render_template('query_results.html', query_args=query_args,
                           results=results, query=query,
                           show_query=show_query, title='Results')


@search.route('/download-results')
def download_results():
    query_args = ast.literal_eval(request.args.get('query_args'))
    query_results = query_db(generate_query(query_args))
    download_path = current_app.config['DOWNLOAD_PATH']
    try:
        filename = make_results_zip(download_path, query_args, query_results)
    except Exception:
        abort(500)
    else:
        try:
            return send_from_directory(download_path, filename, as_attachment=True, cache_timeout=0)
        except FileNotFoundError:
            abort(404)
        finally:
            os.remove(download_path + filename)
