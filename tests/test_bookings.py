import unittest
import requests
import json
from services import bookings
from flask import Flask
from datetime import date as datetime_date
bookings.testing = True


class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5003/bookings"
        self.post_url = "http://localhost:5003/bookings/new"
        self.new_booking_json = """{"date": "2019-11-12", "movie": 5, "user": 4}"""
        self.app = Flask(__name__)
        bookings.db.init_app(self.app)
        with self.app.app_context():
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            bookings.db.create_all()
            self.populate_db()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        bookings.db.init_app(self.app)
        with self.app.app_context():
            bookings.db.drop_all()

    def test_booking_records(self):
        """ Test /bookings/<username> """
        booking = bookings.Booking.query.get(1)
        serialized_book = bookings.booking_schema.dumps(booking)
        with bookings.app.test_client() as get_booking_route:
            response = requests.get(f"{self.url}/{booking.user}")
            response_json = json.dumps(response.json()) # blame python json for this ugly shit
            response_booking = bookings.bookings_schema.loads(response_json)[0] # tough response is in a list, it contains only one object
            self.assertEqual(booking.date, response_booking.date)
            self.assertEqual(booking.movie, response_booking.movie)
            self.assertEqual(booking.user, response_booking.user)

    def populate_db(self):
        """ Populates the database """
        b1 = bookings.Booking(user=1, date=datetime_date(2019, 11, 1), movie=1)
        b2 = bookings.Booking(user=2, date=datetime_date(2019, 11, 2), movie=2)
        b3 = bookings.Booking(user=3, date=datetime_date(2019, 11, 3), movie=3)
        bookings.db.session.add(b1)
        bookings.db.session.add(b2)
        bookings.db.session.add(b3)
        bookings.db.session.commit()

    def test_new_booking(self):
        """ Test for booking creation """
        #fake_booking = bookings.booking_schema.dumps(new_booking)
        with bookings.app.test_client() as new_booking_route:
            # send data as POST form to endpoint:
            response = new_booking_route.post(self.post_url, 
                                        data=self.new_booking_json)
                                        #content_type='application/json')
            # TODO: for some unkown reason passing content_type fucks everything up
            # check result from server with expected fake booking
            self.assertEqual(json.dumps(response.get_json()), self.new_booking_json)


    def test_not_found(self):
        """ Test /showtimes/<date> for non-existent users"""
        invalid_user = "999"
        with bookings.app.test_client() as invalid_user_route: 
            actual_reply = invalid_user_route.get(f"{self.url}/{invalid_user}")
            self.assertEqual(actual_reply.status_code, 404,
                             "Got {actual_reply.status_code} but expected 404")

if __name__ == "__main__":
    unittest.main()
