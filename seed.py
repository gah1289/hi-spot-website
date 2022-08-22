from app import db
from models import User, Board, Payment, Photo, Event, Admin
from datetime import date, time

db.session.remove()
# need to remove sessions or else tables won't drop
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

dan=User(
    first_name='Dan',
    last_name='Jodoin',
    username='danj',
    password='000000',
    email='danj@gmail.com',
    unit=11
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

dan.signup(
    first_name='Dan',
    last_name='Jodoin',
    username='danj',
    password='000000',
    email='danj@gmail.com',
    unit=11
)

bill=User.signup(
    first_name='Bill',
    last_name='Hurley',
    username='bill',
    password='000000',
    email='bill@gmail.com',
    unit=9
)


db.session.commit()

admin=Admin(user_id=1)

president=Board(user_id=3,
position='President')

vp=Board(user_id=5, position='Vice President')

director=Board(user_id=4,
position='Director')


drone_1=Photo(
    url='static/images/drone-1.jpg',
    name='Jesse Holland',
    alt_txt='aerial view of Hi-Spot'
)

drone_2=Photo(
    url='static/images/drone-2.jpg',
    name='Jesse Holland',
    alt_txt='aerial view of Hi-Spot'
)

drone_6=Photo(
    url='static/images/drone-6.jpg',
    name='Jesse Holland',
    alt_txt='aerial view of Hi-Spot'
)

drone_7=Photo(
    url='static/images/drone-7.jpg',
    name='Jesse Holland',
    alt_txt='aerial view of Hi-Spot'
)

drone_8=Photo(
    url='static/images/drone-8.jpg',
    name='Jesse Holland',
    alt_txt='aerial view of Hi-Spot'
)

motel_1=Photo(
    url='static/images/photos-bob/motel-1.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

motel_2=Photo(
    url='static/images/photos-bob/motel-2.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

motel_3=Photo(
    url='static/images/photos-bob/motel-3.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

motel_4=Photo(
    url='static/images/photos-bob/motel-4.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

motel_5=Photo(
    url='static/images/photos-bob/motel-5.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

motel_6=Photo(
    url='static/images/photos-bob/motel-6.jpg',
    name='Bob Pratte',
    alt_txt='motel photo from 2005'
)

brochure=Photo(
    url='static/images/denise/brochure.jpg',
    name='Denise Fishlock',
    alt_txt="photo of brochure"
)

bw_hispot=Photo(
    url='static/images/denise/bw-hispot.jpg',
    name='Reid McCarthy',
    alt_txt='old photo of Hi-Spot'
)

receipt=Photo(
    url='static/images/denise/receipt.jpg',
    name='Reid McCarthy',
    alt_txt="old receipt"
)

fall_meeting=Event(
    title="Fall Meeting 2022",
    description="Hi-Spot Condo association's yearly Fall meeting",
    location_name="Gilford Town Hall",
    location_address="47 Cherry Valley Rd, Gilford, NH 03249",
    date= date(2022, 10,2),
    start_time=time(10,0),
    end_time=time(12,0),
    added_by=1
)

spring_meeting=Event(
    title="Spring Meeting 2022",
    description="Hi-Spot Condo association's yearly Spring meeting",
    location_name="Hi Spot Front Lawn",
    location_address="277 Weirs Blvd. Laconia, NH",
    date= date(2022, 5,2),
    start_time=time(10,0),
    end_time=time(12,0),
    added_by=1
)

db.session.add_all([admin, payment, director, vp,president, drone_1, drone_2, drone_6, drone_7, drone_8, motel_1, motel_2, motel_3, motel_4, motel_5, motel_6, brochure, bw_hispot, receipt, fall_meeting, spring_meeting])

db.session.commit()

