import re
from lamsasweb.search.utils import all_columns
from flask_wtf import FlaskForm
from wtforms import (BooleanField, SelectMultipleField, SelectField,
                     IntegerField, SubmitField, StringField, TextAreaField,
                     ValidationError, Form, Field)
from wtforms.widgets import TextInput, ListWidget, CheckboxInput
from lamsasweb.search.utils import operator_table
from wtforms.validators import DataRequired, Optional, NumberRange


operator_choices = list(operator_table.keys())
greater_than_one = NumberRange(min=1, message='Value must be greater than one')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    @staticmethod
    def at_least_one_selection(form, field):
        if not field.data:
            raise ValidationError('Must have at least one selection')


def db_query_columns(database_seed):
    database_table = database_seed[0]
    database_columns = list(database_seed[1])
    return SelectMultipleField(
        f'Entries from {database_table}',
        choices=database_columns
    )


class DBSimpleQueryForm(FlaskForm):
    tables = MultiCheckboxField('Information Tables',
        choices=list(all_columns.keys()),
        validators=[MultiCheckboxField.at_least_one_selection]
    )
    columns1 = db_query_columns(list(all_columns.items())[0])
    columns2 = db_query_columns(list(all_columns.items())[1])
    order_by = SelectField('Order Results', choices=[''], validators=[
                           Optional()], validate_choice=False)
    limit = IntegerField('Limit Number of Results', validators=[
                         Optional(), greater_than_one], widget=TextInput())
    distinct = BooleanField('Distinct Results')
    submit = SubmitField('Query')


class DBAdvancedQueryForm(DBSimpleQueryForm):
    nulls_last = BooleanField('Empty Values Last')
    offset = IntegerField('Offset Results By',
                          validators=[Optional(), greater_than_one],
                          widget=TextInput())
    where_left = SelectField('\u00a0', choices=[''],
                             validators=[Optional()], validate_choice=False)
    where_operator = SelectField('Data\u00a0Sorting\u00a0Condition',
                                 choices=['', *operator_choices],
                                 validators=[Optional()])
    where_right = StringField('\u00a0', validators=[Optional()])
    show_query = BooleanField('Display Query in SQLite',
                              validators=[Optional()])


class DBRawQueryForm(FlaskForm):
    raw_query = TextAreaField('SQLite Query', validators=[DataRequired()])
    submit = SubmitField('Query')

    def validate_raw_query(form: Form, field: Field) -> None:
        query = field.data
        semicolons = query.count(';')
        match = re.search(';+$', query)
        if not query.endswith(';'):
            raise ValidationError('Query missing terminating semicolon (";")')
        if semicolons > (match.end() - match.start()):
            raise ValidationError('Query can only have one statement')
        if semicolons > 1:
            raise ValidationError(
                'Query can only have one terminating semicolon (";")')
