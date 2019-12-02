from os.path import dirname, realpath
# microframework for webapps
from flask import Flask, request, Response
# local data storage
from flask_sqlalchemy import SQLAlchemy
# data serialization
from marshmallow import Schema, fields, post_load, ValidationError
# to return HTTP status to incoming requests
from http import HTTPStatus as http_status
# read and dump as json data
import json
# exception handling
from werkzeug.exceptions import NotFound

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
root_dir = dirname(realpath(__file__ + '/..'))
db_file = f"sqlite:///{root_dir}/database/movies.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    """ This class maps the database movie model """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Movie: {self.title}>"


class MovieSchema(Schema):
    """ Defines how a Movie instance will be serialized"""
    class Meta:
         """ Add meta attributes here """
         ordered = True # The output will be ordered according to the order that the fields are defined in the class.

    director = fields.String()
    id = fields.Int()
    rating = fields.Int()
    title = fields.String()

    @post_load
    def make_movie(self, data, **kwargs):
        """ Deals with deserialization"""
        return Movie(**data)

# instantiate the schema serializer
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# instructions if you hit '/'
@app.route("/", methods=['GET'])
def hello():
    return json.dumps({
        "uri": "/",
        "subresource_uris": {
            "movies": "/movies",
            "movie": "/movies/<id>"
        }
    })

# add a route to GET showtimes
@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    """ Return all booking instances """
    movies = Movie.query.all()
    serialized_objects = movies_schema.dumps(movies, sort_keys=True, indent=4)

    return Response(
        response=serialized_objects,
        status=http_status.OK,
        mimetype="application/json"
    )

# route to get a movie by its id
@app.route("/movies/<id>", methods=['GET'])
def movie_info(id):
    """ GET a movie by id"""
    movie = Movie.query.get(id)

    if not movie:
        raise NotFound

    serialized_object = movie_schema.dumps(movie, sort_keys=True, indent=4)

    return Response(
    response=serialized_object,
    status=http_status.OK,
    mimetype="application/json"
    )

# add a route to GET all movies
@app.route("/movies", methods=['GET'])
def movie_list():
    """ Return all Movie instances """
    movies = Movie.query.all()
    serialized_objects = movies_schema.dumps(movies, sort_keys=True, indent=4)

    return Response(
        response=serialized_objects,
        status=http_status.OK,
        mimetype="application/json"
    )

# Route for adding a new movie
@app.route("/movies/new", methods=["POST"])
def new_movie():
    """ Make a new movie after a POST request """
    new_movie = ''
    try:
        new_movie = movie_schema.loads(request.data)
    except ValidationError as err:
        pass
        #TODO: send a exception  message
    # save data:
    db.session.add(new_movie)
    db.session.commit()

    return Response(
      response=movie_schema.dumps(new_movie, sort_keys=True, indent=4),
      status=http_status.OK,
      mimetype='application/json'
      )

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5001, debug=True)

