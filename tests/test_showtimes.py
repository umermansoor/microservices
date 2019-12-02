from flask_testing  import TestCase as FlaskTestingCase
from unittest import main
import requests
import json
from flask import Flask
from services import showtimes
from datetime import date as datetime_date
showtimes.testing = True

class TestMoviesService(FlaskTestingCase):
    """ Tests for the Movies service """
    def create_app(self):
        """ Dynamically bind a fake  database to real application """
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        showtimes.db.init_app(app)
        app.app_context().push() # this does the binding
        return app

    def setUp(self):
        """ Get everything ready for tests """
        self.url = "http://localhost:5002/showtimes"
        self.post_url = "http://localhost:5002/showtimes/new"
        self.new_showtime_json = """{"date": "2020-01-01", "movie": 1}"""
        showtimes.db.create_all()
        self.populate_db()

    def tearDown(self):
        """ Ensures that the database is emptied for next unit test """
        showtimes.db.session.remove()
        showtimes.db.drop_all()

    def test_showtime_record(self):
      """ Test if (de)serialization is working properly
      """
      showtime = showtimes.Showtime.query.get(1)
      with showtimes.app.test_client() as get_showtime_route:
        response = requests.get(f"{self.url}/{str(showtime.date)}")
        response_json = json.dumps(response.json())
        # we may get multiple showtimes in reponse but we only want the first
        response_showtime = showtimes.showtimes_schema.loads(response_json)[0]
        self.assertEqual(showtime.date, response_showtime.date)
        self.assertEqual(showtime.movie, response_showtime.movie)
    
    def test_new_showtime(self):
        """ Tests the creation of a new Showtime"""

        fake_showtime = showtimes.showtime_schema.loads(self.new_showtime_json)
        with showtimes.app.test_client() as new_showtime_route:
            # send data as POST form to endpoint:
            response = new_showtime_route.post(self.post_url, data=self.new_showtime_json)

            # check result from server with expected fake booking
            response_showtime_json = json.dumps(response.get_json())
            response_showtime = showtimes.showtime_schema.loads(response_showtime_json)

            self.assertEqual(fake_showtime.date, response_showtime.date)
            self.assertEqual(fake_showtime.movie, response_showtime.movie)
    

    def test_not_found(self):
      """ GET a invalid showtime """
      invalid_showtime = "2018-01-01"
      with showtimes.app.test_client() as invalid_showtime_route: 
        response = invalid_showtime_route.get(f"{self.url}/{invalid_showtime}")
        self.assertEqual(response.status_code, 404,
                             "Got {actual_reply.status_code} but expected 404")
        
    def populate_db(self):
        """ Populates the database """
        s1 = showtimes.Showtime(date=datetime_date(2019, 11, 1), movie=1)
        s2 = showtimes.Showtime(date=datetime_date(2019, 11, 2), movie=2)
        s3 = showtimes.Showtime(date=datetime_date(2019, 11, 3), movie=3)

        showtimes.db.session.add(s1)
        showtimes.db.session.add(s2)
        showtimes.db.session.add(s3)
        showtimes.db.session.commit()

if __name__ == "__main__":
    main()
