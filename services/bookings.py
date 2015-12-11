from services import root_dir, nice_json
from flask import Flask
import json
from werkzeug.exceptions import NotFound


app = Flask(__name__)

with open("{}/database/bookings.json".format(root_dir()), "r") as f:
    bookings = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<username>"
        }
    })


@app.route("/bookings", methods=['GET'])
def booking_list():
    return nice_json(bookings)


@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound

    return nice_json(bookings[username])

if __name__ == "__main__":
    app.run(port=5003, debug=True)

