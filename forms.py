from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateField, TimeField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class UserAddForm(FlaskForm):
    """User register form"""
    first_name=StringField('First Name', validators=[DataRequired()])
    last_name=StringField('Last Name', validators=[DataRequired()])    
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    unit = IntegerField('Unit#', validators=[DataRequired(), NumberRange(min=1,max=18)])

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    reenter_pw=PasswordField('Confirm Password', validators=[Length(min=6)])

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    reenter_pw=PasswordField('Confirm Password', validators=[Length(min=6)])
    old_password = PasswordField('Please Enter Your Old Password to Change', validators=[Length(min=6)])
   

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class BoardMembersForm(FlaskForm):
    """Form for adding and changing members of the board"""
    president=SelectField('President', coerce=int, default= 3)
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

class BankForm(FlaskForm):
    invoice=IntegerField('Invoice Number')
    due=DateField('Due Date')
    amount=DecimalField('Payment Amount', validators=[DataRequired()])
    name=StringField('Full Name', validators=[DataRequired()])    

class CreditCardForm(FlaskForm):
    name=StringField('Full Name', validators=[DataRequired()])
    invoice=IntegerField('Invoice Number', default=1234)
    
    amount=StringField('Payment Amount', validators=[DataRequired()])        
    ccn=StringField('Credit Card Number', validators=[DataRequired()], render_kw={"placeholder": "XXXX XXXX XXXX XXXX"})
    exp_month= StringField('Exp. Month', validators=[DataRequired(), Length(2)], render_kw={"placeholder": "mm"})
    exp_year= StringField('Exp. Year', validators=[DataRequired(), Length(4)], render_kw={"placeholder": "yyyy"})
    security_code=StringField('Security Code', validators=[DataRequired()])

    email=EmailField('Email', validators=[DataRequired()])

    

