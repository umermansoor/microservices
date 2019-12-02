from os.path import dirname, realpath
# microframework for webapps
from flask import Flask, request, Response
# local data storage
from flask_sqlalchemy import SQLAlchemy
# data serialization
from marshmallow import Schema, fields, post_load
# to return HTTP status to incoming requests
from http import HTTPStatus as http_status
# read and dump as json data
import json
# exception handling
from werkzeug.exceptions import NotFound
from datetime import date as datetime_date

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
root_dir = dirname(realpath(__file__ + '/..'))
db_file = f"sqlite:///{root_dir}/database/showtimes.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Showtime(db.Model):
    """ This class maps the database showtime model """
    date = db.Column(db.Date, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Showtime: movie {self.movie} on {self.date}>"


class ShowtimeSchema(Schema):
    """ Defines how a Showtime instance will be serialized"""
    
    class Meta:
         """ Add meta attributes here """
         ordered = True # The output will be ordered according to the order that the fields are defined in the class.

    date = fields.Date()
    id = fields.Int(requeired=False)
    movie = fields.Int()

    @post_load
    def make_showtime(self, data, **kwargs):
        return Showtime(**data)

# instantiate the schema serializer
showtime_schema = ShowtimeSchema()
showtimes_schema = ShowtimeSchema(many=True)

# add root route
@app.route("/", methods=['GET'])
def hello():
    return json.dumps({
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    })

# add a route to GET showtimes
@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    """ Return all booking instances """
    showtimes = Showtime.query.all()
    serialized_objects = showtimes_schema.dumps(showtimes, sort_keys=True, indent=4)

    return Response(
        response=serialized_objects,
        status=http_status.OK,
        mimetype="application/json"
    )


# add a route to GET showtimes for a certain date
@app.route("/showtimes/<date>", methods=['GET'])
def showtimes_record(date):
    # maps a string to a datetime.date object
    date_object = datetime_date(*map(int, date.split('-')))
    showtimes = Showtime.query.filter_by(date=date_object).all()

    if not showtimes:
        raise NotFound

    serialized_objects = showtimes_schema.dumps(showtimes, sort_keys=True, indent=4)

    return Response(
    response=serialized_objects,
    status=http_status.OK,
    mimetype="application/json"
    )

# Route for adding a new movie
@app.route("/showtimes/new", methods=["POST"])
def new_movie():
    """ Make a new movie after a POST request """
    new_showtime = None
    try:
        new_showtime = showtime_schema.loads(request.data)
    except ValidationError as err:
        pass
        #TODO: send a exception  message
    # save data:
    db.session.add(new_showtime)
    db.session.commit()

    return Response(
      response=showtime_schema.dumps(new_showtime, sort_keys=True, indent=4),
      status=http_status.OK,
      mimetype='application/json'
      )

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5002, debug=True)
