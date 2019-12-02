from flask_testing  import TestCase as FlaskTestingCase
from unittest import main
import requests
import json
from flask import Flask
from services import movies
movies.testing = True

class TestMoviesService(FlaskTestingCase):

    def create_app(self):
        """ Dynamically bind a fake  database to real application """
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        movies.db.init_app(app)
        app.app_context().push() # this does the binding
        return app

    def setUp(self):
        """ Get everything ready for tests """
        self.url = "http://localhost:5001/movies"
        self.post_url = "http://localhost:5001/movies/new"
        self.new_movie_json = """{"director": "Alfonso Cuaron", "id": 4, "rating": 10, "title": "Children of Men"}"""
        movies.db.create_all()
        self.populate_db()

    def tearDown(self):
        """ Ensures that the database is emptied for next unit test """
        movies.db.session.remove()
        movies.db.drop_all()

    def test_movie_record(self):
      """ Test if serialization and 
          deserialization are working properly
      """
      movie = movies.Movie.query.get(1)
      with movies.app.test_client() as get_movie_route:
        response = requests.get(f"{self.url}/{movie.id}")
        response_json = json.dumps(response.json())
        response_movie = movies.movie_schema.loads(response_json)
        self.assertEqual(self.fields_dict(response_movie), self.fields_dict(movie))
    
    def test_new_movie(self):
      """ Tests the creation of a new Movie"""
      with movies.app.test_client() as new_movie_route:
          # send data as POST form to endpoint:
          response = new_movie_route.post(self.post_url, 
                                      data=self.new_movie_json)

          # check result from server with expected fake movie
          self.assertEqual(json.dumps(response.get_json()), self.new_movie_json)


    def test_not_found(self):
      """ test GET a invalid movie """
      invalid_movie = "999"
      with movies.app.test_client() as invalid_movie_route: 
        response = invalid_movie_route.get(f"{self.url}/{invalid_movie}")
        self.assertEqual(response.status_code, 404,
                             "Got {actual_reply.status_code} but expected 404")
        
    def populate_db(self):
        """ Populates the database """
        m1 = movies.Movie(rating=10, title="Boyhood", director="Richard Linklater")
        m2 = movies.Movie(rating=8, title="Before Sunset", director="Richard Linklater")
        m3 = movies.Movie(rating=9, title="Waking Life", director="Richard Linklater")

        movies.db.session.add(m1)
        movies.db.session.add(m2)
        movies.db.session.add(m3)
        movies.db.session.commit()
    
    def fields_dict(self, object):
      """ Get an instane of a model and 
          return a dict with fields and values
      """
      column_keys = object.__table__.columns.keys()
      values_dict = dict( (column, getattr(object, column)) for column in column_keys )
      return values_dict

if __name__ == "__main__":
    main()
