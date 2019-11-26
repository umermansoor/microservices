from services import root_dir, nice_json
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus as http_status
import json
from werkzeug.exceptions import NotFound

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
db_file = f"sqlite:///{root_dir()}/database/bookings.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Booking(db.Model):
    """ This class maps the database booking model """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    movie = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Booking: {self.user} @ {self.movie} @ {self.date}>"


# add a route to GET the bookings json
@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<username>"
        }
    })

# add a route to GET bookings json
@app.route("/bookings", methods=['GET'])
def booking_list():
    """ Return all booking instances """
    return nice_json(bookings)

# route to GET bookings json from a specific user
@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    """ Return all booking instances of a certain user """
    if username not in bookings:
        raise NotFound

    return nice_json(bookings[username])

# Route for adding a new booking
@app.route("/bookings/new_booking", methods=["POST"])
def new_booking():
    """ Make a new booking after a POST request """
    response = request.get_json()
    user = response.get("user")
    date = response.get("date")
    movie = response.get("movie")

    # add data:
    try: 
        bookings[user][date].append(movie)
    except:
        bookings[user][date] = [movie]

    # save data:
    save_data(bookings) 

    return Response(
      response=json.dumps({'status': "booked!"}),
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