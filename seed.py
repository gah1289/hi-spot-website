from app import db
from models import User, Board, Payment

db.drop_all()
db.create_all()

gab=User(
    first_name='Gabby',
    last_name='McCarthy',
    username='gah1289',
    password='000000',
    email='gah1289@gmail.com',
    unit=6
)

reid=User(
    first_name='Reid',
    last_name='McCarthy',
    username='rcm9551',
    password='000000',
    email='reidcmccarthy@gmail.com',
    unit=6
)

bob=User(
    first_name='Bob',
    last_name='Pratte',
    username='bobpratte',
    password='000000',
    email='bobpratte@gmail.com',
    unit=16
)

payment=Payment(
    user_id=1,
    stripe_customer_id='fdbvfbvees',
    email='gah1289@gmail.com',
    name='Gabby McCarthy',
    amount=100,
    payment_method='pm_card_visa',
    stripe_payment_id='iuvorwfwrjf32'
)

db.session.add(payment)

gab.signup(first_name='Gabby',
    last_name='McCarthy',
    username='gah1289',
    password='000000',
    email='gah1289@gmail.com',
    unit=6)

reid.signup(first_name='Reid',
    last_name='McCarthy',
    username='rcm9551',
    password='000000',
    email='reidcmccarthy@gmail.com',
    unit=6)

bob.signup(first_name='Bob',
    last_name='Pratte',
    username='bobpratte',
    password='000000',
    email='bobpratte@gmail.com',
    unit=16)

db.session.commit()

president=Board(user_id=3,
position='President')

db.session.add(president)
db.session.commit()

