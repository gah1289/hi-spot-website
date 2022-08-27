"""Payment model tests."""


import os
from sqlite3 import connect
from unittest import TestCase 


os.environ['DATABASE_URL'] = "postgresql:///hispot_test"

from models import db, User, Payment, Event, bcrypt, Admin, Board, Photo

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///hispot_test"

# Now we can import app

from app import app, CURR_USER_KEY, cancel_event


db.session.remove()
db.drop_all()
db.create_all()

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS']=['dont=show-debug-toolbar']


from datetime import date, datetime
import stripe





def create_stripe_checkout_session(card):
    customer=stripe.Customer.create(
            name="Test User",
            email="test@test.com"
        )
    
    payment_method=stripe.PaymentMethod.create(
                    type='card',
                    card=card            
                    )

    payment_intent=stripe.PaymentIntent.create(
            amount=100, # $1
            currency='usd',
            payment_method=payment_method.id,
            receipt_email=customer.email,
            capture_method='automatic'

        )

    stripe.PaymentIntent.confirm(
            payment_intent.id
        )

    product=stripe.Product.create(
            name=f'Invoice 1234'
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

    
    check_payment_intent=payment_intent.retrieve(payment_intent.id)

    return check_payment_intent



class PaymentModelTestCase(TestCase):
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
        
        self.client = app.test_client()

        self.testuser= User.signup(
            first_name="First",
            last_name="Last",
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            unit=1)    
        db.session.commit()
   
    def test_user_model_repr(self):
        """Does the repr method work as expected?"""   
 
        payment=Payment(
            user_id=self.testuser.id,
            invoice=1234,
            due_date="20220825",
            paid_date="20220825",
            email="test@test.com",
            name="First Last",            
            amount=1
        )         
        
        db.session.add(payment)
        db.session.commit()

        self.assertEquals("<Payment: Invoice 1234 for $1.00>", repr(payment))
        self.assertNotEqual("<Payment: Invoice 1234 for $1>", repr(payment))
        self.assertNotEqual("<Payment: Invoice 1234 for $100>", repr(payment))
        self.assertNotEqual("<Payment: Invoice 1234 for 1>", repr(payment))

        

    
    def test_stripe_api(self):
        """Do the stripe API methods work? Does a payment succeed with good card information? Does the payment fail with bad card information?"""        

        today=date.today()

        good_card={
                    'number': '4000000000000077',
                    "cvc": '111',
                    'exp_month':int('08'),
                    "exp_year":int(today.year+5)}
        cvc_fail={
                    'number': '4000000000000101',
                    "cvc": '111',
                    'exp_month':int('08'),
                    "exp_year":int(today.year+5)}
        card_declined={
                    'number': '4000000000000002',
                    "cvc": '111',
                    'exp_month':int('08'),
                    "exp_year":int(today.year+5)}
        
        card_expired={
                    'number': '4000000000000069',
                    "cvc": '111',
                    'exp_month':int('08'),
                    "exp_year":int(today.year+5)}

        # https://stripe.com/docs/testing

        self.assertEqual((create_stripe_checkout_session(good_card)).status, 'succeeded')     
     
        with self.assertRaises(Exception): create_stripe_checkout_session(card_declined)
        with self.assertRaises(Exception): create_stripe_checkout_session(cvc_fail)
        with self.assertRaises(Exception): create_stripe_checkout_session(card_expired)


    
    # def test_website(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         good_card_data={
    #             "name": "Test User",
    #             "invoice": 1234,
    #             "due_date":datetime.today(),
    #             "amount": 1,
    #             "ccn": '4000000000000077',
    #             "exp_month": '01',
    #             "exp_year": str((datetime.today().year)+5),
    #             "security_code": '111',
    #             "email":"test@test.com"
    #         }

    #         resp=c.post("/card", data=good_card_data)
    #         resp=c.get('/', follow_redirects=True)
    #         html=resp.get_data(as_text=True)
    #         self.assertIn('paid', html)



        
        


        


