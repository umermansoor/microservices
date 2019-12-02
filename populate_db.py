from bookings import db as bookings_db
from movies import db as movies_db
from rewards import db as rewards_db
from showtimes import db as showtimes_db
from users import db as users_db
# Models
from bookings import Booking
from movies import Movie
from rewards import Reward
from showtimes import Showtime
from users import User
# timestamp
from datetime import date

# Clean previous databses
bookings_db.drop_all()
movies_db.drop_all()
rewards_db.drop_all()
showtimes_db.drop_all()
users_db.drop_all()

# Create the databases
bookings_db.create_all()
movies_db.create_all()
rewards_db.create_all()
showtimes_db.create_all()
users_db.create_all()

# populate bookings
b1 = Booking(user=1, date=date(2019, 11, 1), movie=1)
b2 = Booking(user=2, date=date(2019, 11, 2), movie=2)
b3 = Booking(user=3, date=date(2019, 11, 3), movie=3)
bookings_db.session.add(b1)
bookings_db.session.add(b2)
bookings_db.session.add(b3)
bookings_db.session.commit()

# populate movies
m1 = Movie(rating=10, title="Boyhood", director="Richard Linklater")
m2 = Movie(rating=8, title="Before Sunset", director="Richard Linklater")
m3 = Movie(rating=9, title="Waking Life", director="Richard Linklater")
movies_db.session.add(m1)
movies_db.session.add(m2)
movies_db.session.add(m3)
movies_db.session.commit()


#populate rewards
r1 = Reward(user=1, score=0)
r2 = Reward(user=2, score=0)
r3 = Reward(user=3, score=0)
rewards_db.session.add(r1)
rewards_db.session.add(r2)
rewards_db.session.add(r3)
rewards_db.session.commit()


#populate showtimes
s1 = Showtime(date=date(2019, 11, 1), movie=1)
s2 = Showtime(date=date(2019, 11, 2), movie=2)
s3 = Showtime(date=date(2019, 11, 3), movie=3)
showtimes_db.session.add(s1)
showtimes_db.session.add(s2)
showtimes_db.session.add(s3)
showtimes_db.session.commit()


# populate users
u1 = User(name="Jim Halpert")
u2 = User(name="Dwight Schrute")
u3 = User(name="Michael Scott")
users_db.session.add(u1)
users_db.session.add(u2)
users_db.session.add(u3)
users_db.session.commit()
