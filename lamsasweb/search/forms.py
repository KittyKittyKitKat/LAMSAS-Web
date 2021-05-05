import re
from flask_wtf import FlaskForm
from wtforms import (BooleanField, SelectMultipleField, SelectField,
                     IntegerField, SubmitField, StringField, TextAreaField,
                     ValidationError, FormMeta, Field)
from wtforms.widgets import TextInput
from lamsasweb.search.utils import operator_table
from wtforms.validators import DataRequired, Optional, NumberRange


operator_choices = list(operator_table.keys())
greater_than_one = NumberRange(min=1, message='Value must be greater than one')


class DBSimpleQueryForm(FlaskForm):
    tables = SelectField('Data Table', choices=[],
                         validators=[DataRequired()], validate_choice=False)
    columns = SelectMultipleField('Columns from Data Table', choices=[],
                                  validators=[DataRequired()],
                                  validate_choice=False)
    order_by = SelectField('Order With', choices=[], validators=[
                           Optional()], validate_choice=False)
    limit = IntegerField('Limit Results To', validators=[
                         Optional(), greater_than_one], widget=TextInput())
    distinct = BooleanField('Distinct Results')
    submit = SubmitField('Query')


class DBAdvancedQueryForm(DBSimpleQueryForm):
    nulls_last = BooleanField('Empty Values Last')
    offset = IntegerField('Offset Results By',
                          validators=[Optional(), greater_than_one],
                          widget=TextInput())
    where_left = SelectField('\u00a0', choices=[],
                             validators=[Optional()], validate_choice=False)
    where_operator = SelectField('Data\u00a0Sorting\u00a0Condition',
                                 choices=operator_choices,
                                 validators=[Optional()])
    where_right = StringField('\u00a0', validators=[Optional()])
    show_query = BooleanField('Display Query in SQLite',
                              validators=[Optional()])


class DBRawQueryForm(FlaskForm):
    raw_query = TextAreaField('SQLite Query', validators=[DataRequired()])
    submit = SubmitField('Query')

    def validate_raw_query(form: FormMeta, field: Field) -> None:
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
