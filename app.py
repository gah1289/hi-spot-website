import os
import stripe 

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from requests import Session
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from secret import secret_stripe_key, publishable_stripe_key

from models import db, connect_db, User, Board

stripe.api_key=publishable_stripe_key

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///hispot'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Home Page"""
    title='Hi-Spot'
    return render_template('home.html', title=title)
