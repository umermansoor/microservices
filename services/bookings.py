from services import root_dir, nice_json
from flask import Flask
import json
from werkzeug.exceptions import NotFound

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
with open("{}/database/bookings.json".format(root_dir()), "r") as data:
    bookings = json.load(data)

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
    return nice_json(bookings)

# route to GET bookings json from a specific user
@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound

    return nice_json(bookings[username])

# Route for adding a new booking
@app.route("bookings/new_booking", method=["POST"])
def new_booking():
    pass


# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5003, debug=True)