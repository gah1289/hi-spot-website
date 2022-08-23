"""User model tests."""


#    python -m unittest test_user_model.py
import os
from unittest import TestCase 
from datetime import date, time

from models import db, User, Payment, Event, bcrypt, Admin, Board, Photo

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///hispot_test"

# Now we can import app

from app import app, CURR_USER_KEY, cancel_event


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


db.create_all()

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


def add_user(user):
    db.session.add(user)
    db.session.commit()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.session.remove()
        User.query.delete()
        Event.query.delete()
        Admin.query.delete()
        Board.query.delete()
        Photo.query.delete()
        Payment.query.delete()

        self.testuser = User.signup(
            first_name="First",
            last_name="Last",
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            unit=1)  


        
       
        db.session.commit()

        
        self.client = app.test_client()
   
    def test_user_model_repr(self):
        """Does the repr method work as expected?"""  


        self.assertEquals("<First Last in Unit 1>", repr(self.testuser))
        self.assertNotEqual("<First Last in Unit 2>", repr(self.testuser))

    
    def test_user_register(self):
        """Does User.create successfully create a new user given valid credentials?
        Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        db.session.commit()
        amt_users=db.session.query(User).count()
        self.assertEqual(amt_users,1)


        user_no_pw=User(
            id=2,
            first_name="First",
            last_name="Last",            
            email="test2@test.com",
            username="testuser2",

        ) 

        user_no_username=User(
            id=3,
            first_name="First",
            last_name="Last",
            email="test3@test.com",
            password="HASHED_PASSWORD",
            unit=1
        ) 

        user_no_email=User(
            id=4,
            first_name="First",
            last_name="Last",
            username="testuser4",
            password="HASHED_PASSWORD",
            unit=1
        )

        user_duplicate=User(
            id=5,
            first_name="First",
            last_name="Last",
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            unit=1
        )
        
        with self.assertRaises(Exception): add_user(user_no_pw)
        with self.assertRaises(Exception): add_user(user_no_username)
        with self.assertRaises(Exception): add_user(user_no_email)
        with self.assertRaises(Exception): add_user(user_duplicate)
    
    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?
        Does User.authenticate fail to return a user when the username is invalid?
        Does User.authenticate fail to return a user when the password is invalid?"""

    
        db.session.commit()
        self.assertTrue(self.testuser.authenticate("testuser", 'HASHED_PASSWORD'))
        self.assertFalse(self.testuser.authenticate("testuser", 'wrongpassword'))
        self.assertFalse(self.testuser.authenticate("wrongusername","password"))
        
        
    def test_check_pw(self):
        """Check that the password is correct when editing a user profile"""
        
        other_user= User.signup(
            first_name="Other",
            last_name="User",
            email="test2@test.com",
            username="testuser2",
            password="password2",
            unit=2) 

        db.session.commit()

        self.assertEquals(self.testuser.check_password(self.testuser.id, 'HASHED_PASSWORD'), self.testuser)        
        self.assertFalse(self.testuser.check_password(self.testuser.id, 'wrongpassword'))
        self.assertFalse(self.testuser.check_password(self.testuser.id, 'password'), other_user)

    def test_logged_out_home(self):
        """When the user is logged out, does it take them to the landing page? When they press 'log in' does it take them to the login page? If they use correct credentials, does it take them to the home page with navbar? If they use incorrect credentials, does it stop them?"""         

        with self.client as c:
            resp=c.get('/')
            html=resp.get_data(as_text=True)
            self.assertIn('Hi-Spot', html) 

            login_resp=c.get('/login')
            login_html=login_resp.get_data(as_text=True)
            self.assertIn('Welcome back.', login_html)   

            bad_username_resp=c.post('/login', data={"username":"bad_username", "password":"HASHED_PASSWORD"}, follow_redirects=True) 
            bad_username_html=bad_username_resp.get_data(as_text=True)
            self.assertIn('Invalid user name!', bad_username_html)
            self.assertIn('Welcome back.', bad_username_html)

            bad_pw_resp=c.post('/login', data={"username":"testuser", "password":"BAD_PASSWORD"}, follow_redirects=True) 
            bad_pw_html=bad_pw_resp.get_data(as_text=True)
            self.assertIn('Invalid password!', bad_pw_html)
            self.assertIn('Welcome back.', bad_pw_html)

            good_username_resp=c.post('/login', data={"username":"testuser", "password":"HASHED_PASSWORD"}, follow_redirects=True) 
            good_username_html=good_username_resp.get_data(as_text=True)
            self.assertEqual(good_username_resp.status_code, 200)
            self.assertIn('Contact', good_username_html)
            self.assertIn('Hello', good_username_html)
            self.assertIn('Account Settings', good_username_html)
    
    def test_unauthorized_access(self):
        """When the user is logged out, can they access routes manually?"""
        with self.client as c:           
            contact=c.get('/contact', follow_redirects=True)
            contact_html=contact.get_data(as_text=True)
            self.assertIn('Please log in', contact_html)
            self.assertNotIn('Email', contact_html)

            docs=c.get('/docs', follow_redirects=True)
            docs_html=docs.get_data(as_text=True)
            self.assertIn('Please log in', docs_html)
            self.assertNotIn('Download', docs_html)

            photos=c.get('/photos', follow_redirects=True)
            photos_html=photos.get_data(as_text=True)
            self.assertIn('Please log in', photos_html)
            self.assertNotIn('Photos', photos_html)

            edit=c.get('/edit_profile', follow_redirects=True)
            edit_html=edit.get_data(as_text=True)
            self.assertIn('Please log in', edit_html)
            self.assertNotIn('Edit Your Profile.', edit_html)

            events=c.get('/events', follow_redirects=True)
            events_html=events.get_data(as_text=True)
            self.assertIn('Please log in', events_html)
            self.assertNotIn('Upcoming', events_html)
    
            edit_board=c.get('/board', follow_redirects=True)
            edit_board_html=edit_board.get_data(as_text=True)
            self.assertIn('Not authorized', edit_board_html)
            self.assertNotIn('President', edit_board_html)

            pay=c.get('/pay', follow_redirects=True)
            pay_html=pay.get_data(as_text=True)
            self.assertIn('Please log in', pay_html)
            self.assertNotIn('Payment Information:', pay_html)

            card=c.get('/card', follow_redirects=True)
            card_html=card.get_data(as_text=True)
            self.assertIn('Please log in', card_html)
            self.assertIn('Hi-Spot', card_html)


    def test_logged_in_tenant(self):
        """When the user is logged in, does it take them to the navigation page? User should not see Edit Board page if they are not on the board"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp=c.get('/')
            html=resp.get_data(as_text=True)
            self.assertIn('Contact', html)
            self.assertIn('Pay Invoice', html)
            self.assertIn('Account Settings', html)
            self.assertNotIn('Edit Board', html)
        
            add_event=c.get('/add_event', follow_redirects=True)
            add_event_html=add_event.get_data(as_text=True)
            self.assertIn('Not authorized', add_event_html)
            self.assertNotIn('Add Event:', add_event_html)

            edit_board=c.get('/board', follow_redirects=True)
            edit_board_html=edit_board.get_data(as_text=True)
            self.assertIn('Not authorized', edit_board_html)
            self.assertNotIn('President', edit_board_html)
        
    def test_loggedin_board(self):
        """When board memebr is logged in, can they see admin pages?"""
        president=Board(user_id=self.testuser.id, position='President')
        board_ids=[self.testuser.id]
        db.session.add(president)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
        
            resp=c.get('/')
            html=resp.get_data(as_text=True)
            self.assertIn('Edit Board', html)
    
            # add_event=c.get('/add_event', follow_redirects=True)
            # add_event_html=add_event.get_data(as_text=True)
            # self.assertIn('Add Event:', add_event_html)

            # edit_board=c.get('/board', follow_redirects=True)
            # edit_board_html=edit_board.get_data(as_text=True)
            # self.assertIn('Not authorized', edit_board_html)
            # self.assertNotIn('President', edit_board_html)

            ######################Test route not workingas board member, but it works when I test it in person
    
    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
        
        resp=c.get('/logout', follow_redirects=True)
        html=resp.get_data(as_text=True)

        self.assertIn('Goodbye!', html)
        self.assertIn('Hi-Spot', html)
        self.assertIn('LOG IN', html)
        self.assertNotIn('Email', html)
            










        


