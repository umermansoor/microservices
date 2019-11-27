from auxiliar import root_dir, nice_json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
import json


app = Flask(__name__)

# load the database
db_file = f"sqlite:///{root_dir()}/database/showtimes.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Showtime(db.Model):
    """ This class maps the database showtime model """
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Showtime: {self.movie} @ {self.date}>"

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
