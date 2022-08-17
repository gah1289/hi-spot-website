from ast import Add
import os
import stripe 
import datetime

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
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
print('*******connect_db(app) in app.py*********')

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        print(f'**************g.user = {g.user}*************')

    else:
        g.user = None
        print('**************No g.user*************')


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def get_board_ids():
    """Get a list of board id's to use in HTML so only board members have access to certain links"""
    board=Board.query.all()
    board_ids=[]
    for member in board:
        board_ids.append(member.user_id)
    return board_ids

board_ids=get_board_ids()

get_board_ids()

@app.route('/')
def home_page():
    """Home Page"""
    

    if not g.user:
        return render_template('home-anon.html')
    board_ids=get_board_ids()
    return render_template('home.html', board_ids=board_ids)


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

    return render_template('user/login.html', form=form)

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
            return render_template('user/register.html', form=form)

        do_login(user)
        flash(f"Welcome, {user.first_name}!", "primary")
        return redirect("/")

    else:
        return render_template('user/register.html', form=form)

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
        
        board=Board.query.all()
        return render_template('contact.html',  board=board, board_ids=board_ids)
    else:
        flash('Please log in or register', 'danger')
        return redirect('/')

@app.route('/docs')
def show_condo_docs():
    """Show condo docs"""
    if g.user:
        
        return render_template('docs.html', board_ids=board_ids)
    else:
        flash('Please log in or register', 'danger')
        return redirect('/')

@app.route('/photos')
def show_photo_gallery():
    """Show photos"""

    if g.user:
        
        photos=Photo.query.all()
        return render_template('photos.html', photos=photos, board_ids=board_ids)
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
            return render_template('user/edit-user.html', form=form)
    
    return render_template('user/edit-user.html', form=form)


@app.route('/events', methods=["GET", "POST"])
def show_upcoming_events():
    """Show upcoming events"""
    if not g.user:
        flash('Please log in', "danger")
        redirect('/')
    current_date=datetime.date.today()
    events=Event.query.all()

    return render_template('events/events.html', events=events, current_date=current_date, board_ids=board_ids)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    """Allow board member to add an event"""
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
    
    return render_template('events/add-event.html', form=form)

@app.route('/events/<id>/cancel', methods=["GET","POST"])
def cancel_event(id):
    """Allow board member to cancel event. The event will stay on the list, but will inform the user that it is cancelled"""  

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        redirect('/')  
    
    event=Event.query.get_or_404(id)    
        
    event.title=event.title,
    event.description='This event has been cancelled',
    event.location_name=event.location_name,
    event.location_address=event.location_address,
    event.date=event.date,
    event.start_time=event.start_time,
    event.end_time=event.end_time,
    event.added_by=g.user.id
        
    db.session.commit()

    flash(f'{event.title} has been cancelled', 'error')
    return redirect('/events')

@app.route('/events/<id>/reschedule', methods=["GET","POST"])
def reschedule_event(id):
    """Allow board member to reschedule event"""

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        redirect('/')

    event=Event.query.get_or_404(id)

    form=AddEventForm(obj=event)

    if form.validate_on_submit():
        event.title=form.title.data,
        event.description='This event has been rescheduled',
        event.location_name=form.location_name.data,
        event.location_address=form.location_address.data,
        event.date=form.date.data,
        event.start_time=form.start_time.data,
        event.end_time=form.end_time.data,
        event.added_by=g.user.id
            
        db.session.commit()

        flash(f'{event.title} has been rescheduled', 'warning')
        return redirect('/events')
    
    return render_template('events/reschedule.html', form=form)

@app.route('/board', methods=["GET", "POST"])
def edit_board_members():
    """Allow board members to edit the board"""
    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', 'error')    

    
    board=[(b.user.id, f'{b.user.first_name} {b.user.last_name}') for b in Board.query.all()]
    form=BoardMembersForm(obj=board)    
    # why isn't it automatically filling up with board member info when I do BoardMembersForm(obj=board)?

    pres=Board.query.filter_by(position='President').one_or_none()
    print('***********')
    print(pres)
    
    user_choices=[(int(u.id), f'{u.first_name} {u.last_name}') for u in User.query.all()]
  
    form.president.choices=user_choices 
    form.vp.choices=user_choices
    form.treasurer.choices=user_choices
    form.secretary.choices=user_choices
    form.director.choices=user_choices 
    form.alternate.choices=user_choices

    # if form.validate_on_submit():        

    #    president=Board(
    #         position='President',
    #         user_id=form.president.data
    #     )
    #    vp=Board(
    #         position='Vice President',
    #         user_id=form.vp.data
    #     )
    #    treasurer=Board(
    #         position='Treasurer',
    #         user_id=form.treasurer.data
    #     )
    #    secretary=Board(
    #         position='Secretary',
    #         user_id=form.secretary.data
    #     )
    #    director=Board(
    #         position='Director',
    #         user_id=form.director.data
    #     )
    #    alternate=Board(
    #         position='Alternate',
    #         user_id=form.alternate.data
    #     )

    #    Board.query.delete()
    #    db.session.add_all([president, vp, treasurer, secretary,director,alternate])
    #    db.session.commit()

    #    flash('Successfully updated board!', 'success')
    #    return redirect('/contact')
    
    return render_template('board.html', form=form, board_ids=board_ids)

@app.route('/events/<id>/delete', methods=["GET", "POST"])
def delete_event(id):
    """Remove event from list in case of user error"""

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        redirect('/')

    event=Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()

    flash(f'Deleted event: {event.title}', 'danger')
    return redirect('/events')





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


