from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange

import email_validator 

board_positions=('pr', 'President'),('vp','Vice President'),('tr', 'Treasurer'), ('sec', 'Secretary'), ('dir', 'Director'), ('alt', 'Alternate')

class UserAddForm(FlaskForm):
    """User register form"""
    first_name=StringField('First Name', validators=[DataRequired()])
    last_name=StringField('Last Name', validators=[DataRequired()])    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    unit = IntegerField('Unit Number', validators=[DataRequired(), NumberRange(min=1,max=18)])

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class BoardMembersForm(FlaskForm):
    """Form for adding and changing members of the board"""
    first_name=StringField('First Name', validators=[DataRequired()])
    last_name=StringField('Last Name', validators=[DataRequired()])
    position=SelectField('Position', choices=[board_positions])

class AddEventForm(FlaskForm):
    title=StringField('Event Name', validators=[DataRequired()])
    description=TextAreaField('Event Description')    
    date=DateField('Date',  validators=[DataRequired()])
    start_time=TimeField('Start Time', validators=[DataRequired()])
    end_time=TimeField('End Time', validators=[DataRequired()])
    location_name=StringField('Name of Location', validators=[DataRequired()])
    location_address=TextAreaField('Address', validators=[DataRequired()])
    