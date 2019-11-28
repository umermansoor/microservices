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
db_file = f"sqlite:///{root_dir}/database/bookings.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Booking(db.Model):
    """ This class maps the database booking model using SQLAlchemy ORM"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    movie = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """ to simple represent an instance of a booking """
        return f"<Booking: user:{self.user} movie: {self.movie} @ {self.date}>"

    def to_schema_dict(self):
        """
        return a simple represented dictionary in the format
        expected by the serializer BookingSchema
        """
        return {"id":self.id, "user":self.user ,"date":self.date, "movie":self.movie}

class BookingSchema(Schema):
    """ Defines how a Booking instance will be serialized"""
    id = fields.Int()
    user = fields.Int()
    date = fields.Date()
    movie = fields.Int()

    @post_load
    def make_booking(self, data, **kwargs):
        return Booking(**data)

# instantiate the schema serializer
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# manuals for this service
@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<user>"
        }
    })

# add a route to GET bookings json
@app.route("/bookings", methods=['GET'])
def booking_list():
    """ Return all booking instances """
    bookings = [booking.to_schema_dict() for booking in Booking.query.all()]
    serialized_objects = bookings_schema.dumps(bookings, sort_keys=True, indent=4)

    return Response(
        response=serialized_objects,
        status=http_status.OK,
        mimetype="application/json"
    )

# route to GET bookings json from a specific user
@app.route("/bookings/<user>", methods=['GET'])
def booking_record(user):
    """ Return all booking instances of a certain user """
    query = Booking.query.filter_by(user=user).all()

    if query is None:
        raise NotFound

    user_bookings = [result.to_schema_dict() for result in query]
    serialized_objects = bookings_schema.dumps(user_bookings, sort_keys=True, indent=4)

    return Response(
    response=serialized_objects,
    status=http_status.OK,
    mimetype="application/json"
    )

# Route for adding a new booking
@app.route("/bookings/new", methods=["POST"])
def new_booking():
    """ Make a new booking after a POST request """

    new_booking = booking_schema.load(request.get_json())
    # save data:
    db.session.add(new_booking)
    db.session.commit()

    #TODO: send new reward point for this user


    return Response(
      response=booking_schema.dumps(new_booking.to_schema_dict(), sort_keys=True, indent=4),
      status=http_status.OK,
      mimetype='application/json'
   )

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5003, debug=True)
