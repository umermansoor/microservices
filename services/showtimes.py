from services import root_dir, nice_json
from flask import Flask
from werkzeug.exceptions import NotFound
import json


app = Flask(__name__)

# load the showtime database
with open("{}/database/showtimes.json".format(root_dir()), "r") as data:
    showtimes = json.load(data)


# add root route
@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    })


# add a route to GET showtimes
@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    return nice_json(showtimes)


# add a route to GET showtimes for a certain date
@app.route("/showtimes/<date>", methods=['GET'])
def showtimes_record(date):
    if date not in showtimes:
        raise NotFound
    #print(showtimes[date])
    return nice_json(showtimes[date])

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5002, debug=True)
