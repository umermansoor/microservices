# microframework for webapps
from flask import Flask, request, Response
# flask user defined services
from auxiliar import root_dir, nice_json
# local data storage
from flask_sqlalchemy import SQLAlchemy
# data serialization
from marshmallow import Schema, fields
# to return HTTP status to incoming requests
from http import HTTPStatus as http_status
# read and dump as json data
import json
# exception handling
from werkzeug.exceptions import NotFound

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
db_file = f"sqlite:///{root_dir()}/database/bookings.db"
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
        return f"<Booking: {self.user} @ {self.movie} @ {self.date}>"

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

# instantiate the schema serializer
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# add a route to GET the bookings json
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

# TOOD: Route for adding a new booking
@app.route("/bookings/new", methods=["POST"])
def new_booking():
    """ Make a new booking after a POST request """
    json_response = request.get_json()
    user = json_response.get("user")
    date = json_response.get("date")
    movie = json_response.get("movie")

    # add data:
    new_booking = Booking(user=user, data=date, movie=movie)
    # save data:
    db.session.add(new_booking)
    db.session.commit()

    return Response(
      response=booking_schema.dumps(new_booking.to_schema_dict(), sort_keys=True, indent=4),
      status=http_status.OK,
      mimetype='application/json'
   )   

def save_data(data):
    """ This method saves bookings to the json file """
    with open("{}/database/bookings.json".format(root_dir()), "w") as file:
        json.dump(data, file, sort_keys=True, indent=4) 

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5003, debug=True)
