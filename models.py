import email
from email.policy import default
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

import stripe


bcrypt = Bcrypt()


class User(db.Model):
    """User in the HiSpot Database"""
    __tablename__='users'
  

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )  

    first_name=db.Column(
        db.Text,
        nullable=False
    )

    last_name=db.Column(
        db.Text,
        nullable=False
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False
    )

    unit=db.Column(db.Integer)


    def __repr__(self):
        return f"<{self.first_name} {self.last_name} in Unit {self.unit}>"
    
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
    )

    position=db.Column(db.String, unique=True)

    user=db.relationship('User', backref="board")

    def __repr__(self):
        return f"<Board Member: {self.position}>"

class Photo(db.Model):
    """Pictures for photo gallery"""

    __tablename__="photos"

    id= db.Column(
        db.Integer,
        primary_key=True,
    )

    url=db.Column(db.Text, nullable=False, unique=True)

    name=db.Column(
        db.Text,
        nullable=False,
    )

    alt_txt=db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<Photo Member: {self.url}>"

    print('***********CREATED BOARD TABLE')

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

    stripe_customer_id=db.Column(
        db.Text
  
    )
    
    checkout_id=db.Column(
        db.Text

    )

    payment_status =db.Column(
        db.Text,
    
    )


    invoice=db.Column(db.Integer)
    paid_date=db.Column(db.Date)


    user=db.relationship('User', backref="payments")

    

    def __repr__(self):
        return f"<Payment: Invoice {self.invoice} for ${self.amount:.2f}>"  
        # https://stackoverflow.com/questions/20457038/how-to-round-to-2-decimals-with-python
    
    print('***************IMPORTED USER')
    
class Event(db.Model):
    """Condo-related events"""

    __tablename__="events"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title=db.Column(
        db.Text,
        nullable=False
    )

    description=db.Column(
        db.Text,
        default=None
    )

    location_name=db.Column(
        db.Text,
        nullable=False
    )

    location_address=db.Column(
        db.Text,
        nullable=False
    )

    date=db.Column(
        db.Date,
        nullable=False,
    )

    start_time=db.Column(db.Time,nullable=False)
    end_time=db.Column(db.Time,nullable=False)

    added_by=db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user=db.relationship('User', backref="events")

    def __repr__(self):
        return f"<Event: {self.title}>"

    print('***********IMPORTED EVENT')    

class Admin(db.Model):
    """Admin in the HiSpot Database"""
    __tablename__='administrators'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )  

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
    )

    user=db.relationship('User')

    def __repr__(self):
        return f"<Admin: {self.username}>"

    
    


def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)
    
    return app


