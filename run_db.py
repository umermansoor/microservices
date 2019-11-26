# databases
from services.bookings import db as booking_db
from services.movies import db as movies_db
from services.rewards import db as rewards_db
from services.showtimes import db as showtimes_db
from services.users import db as users_db
# Models
from services.bookings import Book
from services.movies import Movie
from services.rewards import Reward
from services.showtimes import Showtime
from services.users import User
# timestamp
from datetime import datetime

# Create the databases
booking_db.create_all()
movies_db.create_all()
rewards_db.create_all()
showtimes_db.create_all()
users_db.create_all()

# populate bookings
b1 = Booking(user="1", date=datetime(2019, 11, 1), movie="1")
b2 = Booking(user="2", date=datetime(2019, 11, 2), movie="2")
b3 = Booking(user="3", date=datetime(2019, 11, 3), movie="3")

booking_db.session.add(b1)
booking_db.session.add(b2)
booking_db.session.add(b3)

booking_db.session.commit()

# populate movies
b1 = Booking(user="1", date=datetime(2019, 11, 1), movie="1")
b2 = Booking(user="2", date=datetime(2019, 11, 2), movie="2")
b3 = Booking(user="3", date=datetime(2019, 11, 3), movie="3")

booking_db.session.add(b1)
booking_db.session.add(b2)
booking_db.session.add(b3)

booking_db.session.commit()
