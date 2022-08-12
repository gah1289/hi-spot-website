import email
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import stripe


bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the HiSpot Database"""
    __tablename__='users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )  

    first_name=db.Column(
        db.Text,
        nullable=False,
    )

    last_name=db.Column(
        db.Text,
        nullable=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    unit=db.Column(db.Integer)

    board=db.relationship('Board')

    def __repr__(self):
        return f"<{self.first_name} {self.last_name} in Unit {self.unit}>"
    
    # def is_board_member(self, board_member):
    #     """Is this user on the board?"""
    #     board_list=[user for user in self.board]


    @classmethod
    def signup(cls, first_name, last_name, username, password, email, unit):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(            
            first_name=first_name,
            last_name=last_name,
            username=username,  
            password=hashed_pwd,
            email=email,
            unit=unit
        )        
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
            If it can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def check_password(cls, user_id, password):
        """Check that the password is correct when editing a user profile"""
        user = cls.query.get_or_404(user_id)


        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            user.password=bcrypt.generate_password_hash(password).decode('UTF-8')            
            db.session.commit()
            if is_auth:                
                return user

        return False

class Board(db.Model):
    """Members of the board"""
    __tablename__="board_members"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    position=db.Column(db.String, unique=True)

    user=db.relationship('User')

class Payment(db.Model):
    """Person trying to make a payment online"""

    __tablename__="payments"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    stripe_customer_id=db.Column(
        db.Text,
        nullable=False
    )
    # customer id - get from API. stripe.Customer.retrieve(id, apikey=apikey)
   
    email=db.Column(
        db.Text,
        nullable=False
    )
    name=db.Column(
        db.Text,
        nullable=False
    )
    amount=db.Column(
        db.Float,
        nullable=False,
        default='0'
    )
    payment_method=db.Column(
        db.Text,
        nullable=False
    )

    stripe_payment_id=db.Column(
        db.Text,
        nullable=False
    )

    user=db.relationship('User')

    def create_customer(name, email, payment_method):
        """Create customer with scalar values"""
        customer = stripe.Customer.create(
            name=name,
            email=email,
            payment_method=payment_method
            )
        return customer
    
    def update_customer(name, email, payment_method):
        """modify customer"""
        modified_customer=stripe.Customer.modify(
            name=name,
            email=email,
            payment_method=payment_method
        )
        return modified_customer
    
    def delete_customer(id):
        """Delete customer"""
        stripe.customer.delete(id=id)
        return True

    def create_payment_intent(amount, payment_method, receipt_email):
        """Create a payment intent to confirm"""
        payment_intent=stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method=payment_method,
            receipt_email=receipt_email
        )
        return payment_intent
    
    def confirm_payment_intent(amount, payment_id, payment_method, receipt_email):
        """confirm payment intent"""
        payment_intent=stripe.PaymentIntent.confirm(payment_id, 
            amount=amount,
            currency='usd',
            payment_method=payment_method,
            receipt_email=receipt_email
        )
        return payment_intent    



def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)

