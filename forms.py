from unicodedata import category
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, DateField, TimeField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange

import email_validator 

class UserAddForm(FlaskForm):
    """User register form"""
    first_name=StringField('First Name', validators=[DataRequired()])
    last_name=StringField('Last Name', validators=[DataRequired()])    
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    unit = IntegerField('Unit Number', validators=[DataRequired(), NumberRange(min=1,max=18)])

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class BoardMembersForm(FlaskForm):
    """Form for adding and changing members of the board"""
    president=SelectField('President', coerce=int)
    vp=SelectField('Vice President', coerce=int)
    treasurer=SelectField('Treasurer', coerce=int)
    secretary=SelectField('Secretary', coerce=int)
    director=SelectField('Director', coerce=int)
    alternate=SelectField('Alternate', coerce=int)

    password=PasswordField('Password', validators=[DataRequired()])


class AddEventForm(FlaskForm):
    title=StringField('Event Name', validators=[DataRequired()])
    description=TextAreaField('Event Description')    
    date=DateField('Date',  validators=[DataRequired()])
    start_time=TimeField('Start Time', validators=[DataRequired()])
    end_time=TimeField('End Time', validators=[DataRequired()])
    location_name=StringField('Name of Location', validators=[DataRequired()])
    location_address=TextAreaField('Address', validators=[DataRequired()])
    