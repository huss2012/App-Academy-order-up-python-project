from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired




class LoginForm(FlaskForm):
    employee_number = StringField('Employee number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AssingTableForm(FlaskForm):
    table = SelectField("Open Table", choices=[], validators=[DataRequired()])
    employee = SelectField("Server", choices=[], validators=[DataRequired()])
    assing = SubmitField("Assing")

class CloseTableForm(FlaskForm):
    close_table = SubmitField('Close Table')


class AddToOrderForm(FlaskForm):
    test1 = BooleanField("Test1")
    test2 = BooleanField("Test2")
    add_to_order_but = SubmitField("ADD TO ORDER")
