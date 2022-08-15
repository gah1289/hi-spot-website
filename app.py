import os
import stripe 
import datetime

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from requests import Session
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from secret import secret_stripe_key, fa_token

from models import db, connect_db, User, Board, Photo, Event, bcrypt
from forms import AddEventForm, UserAddForm, LoginForm, BoardMembersForm

publishable_stripe_key = 'pk_test_51LUyPRBQnQlv8BXXSDB4CdqhM5Rpnhx4lWMAcSUdjbORzGhy4h2JKYOtzFhcp8KhDc87cQPAOIE23Gc18Kkzlfs200S6ufWWXU'
# test mode


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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home_page():
    """Home Page"""
    title='Hi-Spot'

    if not g.user:
        return render_template('home-anon.html', title=title)
    return render_template('home.html', title=title)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():   
        user_exists=User.query.filter_by(username=form.username.data).first()
        if not user_exists: 
            flash('Invalid user name!', 'danger') 
            return redirect('/login')   

        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:            
            do_login(user)
            flash(f"Hello, {user.first_name}!", "primary")
            return redirect("/")

        flash("Invalid password!", 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                unit=form.unit.data,
                username=form.username.data,
                password=form.password.data,              
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)

        do_login(user)
        flash(f"Welcome, {user.first_name}!", "primary")
        return redirect("/")

    else:
        return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()
    flash('Goodbye!', 'primary')

    return redirect('/')

@app.route('/contact')
def show_contact_page():
    """Show contact info"""
    if g.user:
        title="Contact Hi-Spot"
        board=Board.query.all()
        return render_template('contact.html', title=title, board=board)
    else:
        flash('Please log in or register', 'danger')
        return redirect('/')

@app.route('/docs')
def show_condo_docs():
    """Show condo docs"""
    if g.user:
        title='Hi-Spot Condo Docs'
        return render_template('docs.html', title=title)
    else:
        flash('Please log in or register', 'danger')
        return redirect('/')

@app.route('/photos')
def show_photo_gallery():
    """Show photos"""

    if g.user:
        title='Hi-Spot Photos'
        photos=Photo.query.all()
        return render_template('photos.html', title=title, photos=photos)
    else:
        flash('Please log in or register', 'danger')
        return redirect('/')

@app.route('/edit_profile', methods=["GET", "POST"])
def edit_user_info():
    """Allow user to edit profile information, must confirm password"""
    if not g.user:
        flash('Please log in', "danger")
        redirect('/')
    
    form=UserAddForm(obj=g.user)

    if form.validate_on_submit(): 
        try:
            password_correct=User.check_password(g.user.id, form.password.data)
            if password_correct:
                g.user.first_name=form.first_name.data,
                g.user.last_name=form.last_name.data,
                g.user.email=form.email.data,
                g.user.unit=form.unit.data,
                g.user.username=form.username.data,
                g.user.password=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')   
            else:
                form.password.errors=["Password is incorrect"]
            db.session.commit()
            flash(f"Updated {g.user.username}'s profile!", "success") 
        except IntegrityError:
            db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('edit_user.html', form=form)
    
    return render_template('edit_user.html', form=form)


@app.route('/events', methods=["GET", "POST"])
def show_upcoming_events():
    """Show upcoming events"""
    if not g.user:
        flash('Please log in', "danger")
        redirect('/')
    current_date=datetime.date.today()
    events=Event.query.all()
    board=Board.query.all()
    board_ids=[]
    for member in board:
        board_ids.append(member.user_id)
    return render_template('events.html', events=events, current_date=current_date, board_ids=board_ids)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    """Allow board member to add an event"""
    board=Board.query.all()
    board_ids=[]
    for member in board:
        board_ids.append(member.user_id)
    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        redirect('/')
 
    form=AddEventForm()
    if form.validate_on_submit():
        event=Event(
            title=form.title.data,
            description=form.description.data,
            location_name=form.location_name.data,
            location_address=form.location_address.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            added_by=g.user.id
        )

        db.session.add(event)
        db.session.commit()

        flash(f'Successfully added event: {event.title}!')
        return redirect('/events')
    
    return render_template('add-event.html', form=form)

@app.template_filter('date')
def date_format(value, format="%B %d, %Y"):
    """Converts date to more readable format. 
    https://www.programiz.com/python-programming/datetime/strftime"""
    return value.strftime(format)


@app.template_filter('time')
def date_format(value, format="%-I:%M %p"):
    """Converts time to more readable format"""
    return value.strftime(format)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('custom-404.html')
