import os
import csv
import datetime
import sqlite3
import re
from collections import defaultdict
from zipfile import ZipFile
from flask import g

all_columns = {
    'Informants': [
        'Informant',
        'Project',
        'Sex',
        'Age',
        'Ethnicity',
        'Education Level',
        'Occupation',
        'Town/City',
        'County',
        'State',
        'Latitude',
        'Longitude',
        'Fieldworker',
        'Year Interviewed',
        'Notes'
    ],
    'Responses': [
        'Informant',
        'Lexical Item',
        'Comments',
        'Transcription',
        'Page Number',
        'Line Number'
    ]
}
operator_table = {
    'Is Equal To': '=',
    'Is Not Equal To': '!=',
    'Is Greater Than': '>',
    'Is Less Than': '<',
    'Is Greater Than or Equal To': '>=',
    'Is Less Than or Equal To': '<=',
    'Contains Substring': 'LIKE',
    'Excludes Substring': 'NOT LIKE',
    'Matches Regex': 'GLOB'
}
reversed_operator_table = {value: key for key, value in operator_table.items()}


def query_args_from_form(form, ignore_fields):
    args_dict = {fieldname: value for fieldname, value in form.data.items()
            if fieldname not in ignore_fields}
    cols2 = args_dict['columns2']
    try:
        cols2.remove('Informant')
    except ValueError:
        pass
    columns = args_dict['columns1'] + cols2
    args_dict['columns'] = columns
    return args_dict


def col_to_schema(col):
    return re.sub('[^0-9a-zA-Z]+', '_', col)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('file:LAMSAS.db?mode=ro', uri=True)
    return db


def generate_query(args_dict):
    args_dict = defaultdict(lambda: None, args_dict)
    distinct_clause = ' DISTINCT ' if args_dict['distinct'] else ' '
    cols = ', '.join([col_to_schema(col) for col in args_dict['columns']])
    all_tables = args_dict['tables']
    table = all_tables[-1]
    join_tables = all_tables[:-1] if len(all_tables) > 1 else []
    join_clause = ''
    if join_tables:
        for j_table in join_tables:
            join_clause += f' INNER JOIN {j_table} USING(Informant)'
    ob = args_dict['order_by']
    if ob and ob.endswith(' DESC'):
        asc_desc = ' DESC'
        ob = ob[:-5]
    elif ob and ob.endswith(' ASC'):
        asc_desc = ' ASC'
        ob = ob[:-4]
    else:
        asc_desc = ''
    ob = col_to_schema(ob)
    order_by_clause = ' ORDER BY ' + ob if ob else ''
    if args_dict['nulls_last'] and asc_desc == ' ASC':
        nulls_last_clause = ' NULLS LAST '
    elif args_dict['nulls_last'] and asc_desc == ' DESC':
        nulls_last_clause = ' NULLS FIRST '
    else:
        nulls_last_clause = ''
    limit_clause = ' LIMIT ' + \
        str(args_dict['limit']) if args_dict['limit'] else ''
    offset_clause = ' OFFSET ' + \
        str(args_dict['offset']) if args_dict['offset'] else ''
    if args_dict['where_left']:
        print(args_dict['where_operator'])
        print(operator_table[args_dict['where_operator']])
        where_op = operator_table[args_dict['where_operator']]
        fixed_wf = col_to_schema(args_dict['where_left'])
        fixed_wr = f"'{args_dict['where_right']}'"
        if where_op == 'LIKE':
            fixed_wr = f"'%{fixed_wr[1:-1]}%'"
        where_clause = f" WHERE {fixed_wf} {where_op} {fixed_wr}"
    else:
        where_clause = ''
    query = ('SELECT' + distinct_clause + f'{cols} FROM {table}' +
        join_clause + where_clause + order_by_clause + asc_desc +
        nulls_last_clause + limit_clause + offset_clause + ';')
    return query


def get_args_from_query(raw_query):
    query = raw_query.replace(', ', ',').replace(';', '')
    args_dict = {}
    for keyword in ['DISTINCT', 'NULLS LAST', 'NULLS FIRST']:
        if keyword in query:
            key = col_to_schema(keyword.lower().replace('FIRST', 'LAST'))
            args_dict[key] = True
            query = query.replace(keyword + ' ', '')
    if 'ASC' in query:
        asc_desc = ' ASC'
        query = query.replace('ASC ', '')
    elif 'DESC' in query:
        asc_desc = ' DESC'
        query = query.replace('DESC ', '')
    else:
        asc_desc = ''
    for keyword in ['FROM', 'SELECT', 'LIMIT', 'OFFSET', 'ORDER BY']:
        match = re.search(keyword+' [^ ]*', query, re.IGNORECASE)  # noqa: E226
        key = col_to_schema(keyword.lower())
        if match:
            start, end = match.span()
            clause = query[start:end]
            value = clause.split()[-1]
            if keyword == 'SELECT':
                key = 'columns'
                if value == '*':
                    value = all_columns[args_dict['tables']]
                else:
                    value = value.split(',')
            if keyword == 'FROM':
                key = 'tables'
            if keyword == 'ORDER BY':
                value += asc_desc if asc_desc else ' ASC'
            try:
                value = int(value)
            except (ValueError, TypeError):
                pass
            args_dict[key] = value
            query = query.replace(clause, '')
            query = query.strip()
        else:
            args_dict[key] = ''
    where = query.split()
    if where:
        args_dict['where_left'] = where[1]
        args_dict['where_operator'] = reversed_operator_table[where[2]]
        args_dict['where_right'] = where[3].replace("'", '').replace('%', '')
    return args_dict


def query_db(query):
    try:
        query = get_db().execute(query)
    except Exception as e:
        raise type(e)(*e.args)
    else:
        result = [[*row] for row in query]
        return result


def get_downloads_folder(root_file):
    dirname = os.path.dirname(root_file)
    downloads_folder = os.path.join(dirname, 'static/')
    return downloads_folder


def make_results_zip(downloads_path, args_dict, query_results):
    if args_dict is None or query_results is None:
        raise TypeError("Got 'NoneType', expected valid argument")
    now = datetime.datetime.now()
    iso = now.isoformat().rpartition(':')[0]
    filename_csv = f'LAMSAS_Search_Results_{iso}.csv'
    filename_meta = f'LAMSAS_Search_META_{iso}.txt'
    filename_zip = f'LAMSAS_Search_{iso}.zip'
    with open(downloads_path + filename_meta, 'w') as meta_file:
        lines = [
            'LAMSAS Search Metadata:',
            f'Created on: {now}',
            f'SQLite Query: {generate_query(args_dict)}',
            f"Total Number of Results: {len(query_results)} rows with "
            f"{len(args_dict['columns'])} columns of data",
            f"Results are located in '{filename_csv[:-4]}' in CSV format, "
            "which can be opened by any spreadsheet editor."
        ]
        for line in lines:
            meta_file.write(line + '\n')
    with open(downloads_path + filename_csv, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(args_dict['columns'])
        for line in query_results:
            writer.writerow(line)
    with ZipFile(downloads_path + filename_zip, 'w') as zip_file:
        zip_file.write(downloads_path + filename_meta, filename_meta)
        zip_file.write(downloads_path + filename_csv, filename_csv)
    os.remove(downloads_path + filename_meta)
    os.remove(downloads_path + filename_csv)
    return filename_zip
