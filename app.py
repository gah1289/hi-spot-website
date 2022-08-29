import os
import stripe, logging
import datetime


from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
# from requests import Session
from sqlalchemy.exc import IntegrityError


# from secret import secret_stripe_key, fa_token

from models import Admin, db, connect_db, User, Board, Photo, Event, bcrypt, Admin
from forms import AddEventForm, UserAddForm, LoginForm, BoardMembersForm,  CreditCardForm

stripe_key = 'sk_test_51LUyPRBQnQlv8BXXTCh2ILwiMp3C2t25xOkVkmbOUZhY5BFSTHgRLItXOGrIlL4ep2VpDghjgYjt4DgKIxE1ONap00rkA9Vk1X'
# test mode



stripe.api_key=stripe_key

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///hispot'))
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',"postgresql:///hispot").replace("://", "ql://", 1)

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

def get_board_ids():
    """Get a list of board id's to use in HTML so only board members have access to certain links"""
    board=Board.query.all()
    admin=Admin.query.all()
    board_ids=[]
    for member in board:
        board_ids.append(member.user_id)
    for member in admin:
        board_ids.append(member.user_id)
    return board_ids

board_ids=get_board_ids()

get_board_ids()

@app.route('/')
def home_page():
    """Home Page"""
    
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
            flash(f"Hello, {user.first_name}!", "info")
            return redirect("/")

        flash("Invalid password!", 'danger')

    return render_template('user/login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: show error
    and re-present form. If passwords do not match, show error.
    """

    form = UserAddForm()

    usernames=[]
    for user in User.query.all():
        usernames.append(user.username)

    if form.validate_on_submit():
        if form.username.data in usernames:
            form.username.errors=["Username already taken."]
        if form.reenter_pw.data != form.password.data:
            form.password.errors=["Passwords do not match."]
            print('*******************')
            print(f'{form.reenter_pw.data} != {form.password.data}')
        else:        
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
                flash("Error. Please try again", 'danger')
                return render_template('user/register.html', form=form)

            do_login(user)
            flash(f"Welcome, {user.first_name}!", "info")
            return redirect("/")
    
    return render_template('user/register.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()
    flash('Goodbye!', 'info')

    return redirect('/')

@app.route('/contact')
def show_contact_page():
    """Show contact info"""
    if g.user:
        
        board=Board.query.all()
        return render_template('contact.html',  board=board, board_ids=board_ids)
    else:
        flash('Please log in or register', 'info')
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
       
    photos=Photo.query.all()
    return render_template('photos.html', photos=photos, board_ids=board_ids)
   

@app.route('/edit_profile', methods=["GET", "POST"])
def edit_user_info():
    """Allow user to edit profile information, must confirm password"""
    if not g.user:
        flash('Please log in', "danger")
        return redirect('/')
    
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
        return redirect('/')

    current_date=datetime.date.today()
    events=Event.query.all()

    return render_template('events/events.html', events=events, current_date=current_date, board_ids=board_ids)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    """Allow board member to add an event"""
    if not g.user or g.user.id not in board_ids:
        flash('Not authorized', "danger")
 
        
        return redirect('/')
   

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

        flash(f'Successfully added event: {event.title}!', 'info')
        return redirect('/events')
    
    return render_template('events/add-event.html', form=form, board_ids=board_ids)

@app.route('/events/<id>/cancel', methods=["GET","POST"])
def cancel_event(id):
    """Allow board member to cancel event. The event will stay on the list, but will inform the user that it is cancelled"""  

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        return redirect('/')  
    
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

    flash(f'{event.title} has been cancelled', 'warning')
    return redirect('/events')

@app.route('/events/<id>/reschedule', methods=["GET","POST"])
def reschedule_event(id):
    """Allow board member to reschedule event"""

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        return redirect('/')

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
    if not g.user or g.user.id not in board_ids:
        flash('Not authorized', 'danger') 
        return redirect('/')   
    
    president=Board.query.filter_by(position="President").one_or_none()
    vp=Board.query.filter_by(position="Vice President").one_or_none()
    treasurer=Board.query.filter_by(position="Treasurer").one_or_none()
    alternate=Board.query.filter_by(position="Alternate").one_or_none()
    director=Board.query.filter_by(position="Director").one_or_none()
    secretary=Board.query.filter_by(position="Secretary").one_or_none()


    form=BoardMembersForm(president=president.user_id, vp=vp.user_id, treasurer=treasurer.user_id, secretary=secretary.user_id, director=director.user_id, alternate=alternate.user_id)    

      
    user_choices=[('0', '-- select an option --')] +[(int(u.id), f'{u.first_name} {u.last_name}') for u in User.query.all()]
    # without 0, select option first, all values default to user_id=1 https://lightrun.com/answers/wtforms-flask-wtf-add-empty-option-in-selectfield   
  
    form.president.choices=  user_choices 
    form.vp.choices=user_choices
    form.treasurer.choices=user_choices
    form.secretary.choices=user_choices
    form.director.choices=user_choices 
    form.alternate.choices=user_choices


    if form.validate_on_submit():
        try:       
            president.user_id=form.president.data
            vp.user_id=form.vp.data
            treasurer.user_id=form.treasurer.data
            alternate.user_id=form.alternate.data
            secretary.user_id=form.secretary.data
            director.user_id=form.director.data 
            db.session.commit()   
        except: 
            president=Board(
                position='President',
                user_id=form.president.data
                )
            vp=Board(
                position='Vice President',
                    user_id=form.vp.data
                )
            treasurer=Board(
                    position='Treasurer',
                    user_id=form.treasurer.data
                )
            secretary=Board(
                    position='Secretary',
                    user_id=form.secretary.data
                    )
            director=Board(
                    position='Director',
                    user_id=form.director.data
                    )
            alternate=Board(
                    position='Alternate',
                    user_id=form.alternate.data
                    )
            Board.query.delete()
            db.session.add_all([president,vp,treasurer,secretary,director,alternate])
            db.session.commit()

            flash('Successfully updated board!', 'success')
            return redirect('/contact')
    
    return render_template('board.html', form=form, board_ids=board_ids)

@app.route('/events/<id>/delete', methods=["GET", "POST"])
def delete_event(id):
    """Remove event from list in case of user error"""

    if not g.user and g.user.id not in board_ids:
        flash('Not authorized', "danger")
        return redirect('/')

    event=Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()

    flash(f'Deleted event: {event.title}', 'danger')
    return redirect('/events')


@app.route('/pay')
def ask_payment_method():
    '''Ask user if they want to pay by cc or bank'''
    if not g.user:
        flash('Please log in', "danger")
        return redirect('/')
    form=CreditCardForm()

    return render_template('pay/plain_cc.html', form=form, board_ids=board_ids)

@app.route('/card', methods=["GET", "POST"])
def show_payment_form():
    """Show payment form"""
    if not g.user:
        flash('Please log in', "danger")
        return redirect('/')
    
    form=CreditCardForm()

    if form.validate_on_submit(): 
        try:
            customer=stripe.Customer.create(
                name=form.name.data,
                email=form.email.data
                )

            payment_method=stripe.PaymentMethod.create(
                type='card',
                card={
                    'number': form.ccn.data,
                    "cvc": form.security_code.data,
                    'exp_month':int(form.exp_month.data),
                    "exp_year":int(form.exp_year.data)},            
                )
        

            try:
                payment_intent=stripe.PaymentIntent.create(
                    amount=((int(form.amount.data))*100),
                    currency='usd',
                    payment_method=payment_method.id,
                    receipt_email=form.email.data,
                    capture_method='automatic'
                )
            except stripe.error.CardError as e:
                logging.error("A payment error occurred: {}".format(e.user_message))
            except stripe.error.InvalidRequestError:
                logging.error("An invalid request occurred.")
            except Exception:
                logging.error("Another problem occurred, maybe unrelated to Stripe.")
            else:
                logging.info("No error.")

            
            stripe.PaymentIntent.confirm(
                payment_intent.id
            )
   
            product=stripe.Product.create(
                name=f'Invoice {form.invoice.data}'
            )

            price=stripe.Price.create(
                product=product.id,
                currency='usd',
                unit_amount=payment_intent.amount
            )

            checkout=stripe.checkout.Session.create(
                    success_url='http://127.0.0.1:5000/',
                    cancel_url="http://127.0.0.1:5000/pay",
                    mode="payment",
                    customer=customer.id,   
                    line_items=[
                        {
                            "price": price.id,
                            "quantity": 1
                        }
                    ]            
                )
                      
          
            flash(f'Successfully paid invoice {form.invoice.data}!', 'success')
            return redirect('/')

        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
            flash("A payment error occurred: {}".format(e.user_message))
            # pass
            return redirect('/pay')
        except stripe.error.AuthenticationError as e:
            flash("A payment error occurred: {}".format(e.user_message))
            # pass
            return redirect('/pay')
        except stripe.error.APIConnectionError as e:
            flash("A payment error occurred: {}".format(e.user_message))
            # pass
            return redirect('/pay')
        except stripe.error.StripeError as e:
            flash("A payment error occurred: {}".format(e.user_message))
            # pass
            return redirect('/pay')       
        except Exception as e:
            flash("A payment error occurred. Please check that the credit card number you entered is correct", "danger")
            # pass
            return redirect('/pay') 
        
    else: 
        payment_intent=payment_intent.retrieve(payment_intent.id)
        flash(f'Payment Failed: {payment_intent.last_payment_error.message}', 'danger') 
    
    return redirect ('/pay')

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


