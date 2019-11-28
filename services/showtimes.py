# microframework for webapps
from flask import Flask, request, Response
# flask user defined services
from auxiliar import root_dir, nice_json
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
from datetime import date

# instantiate a flask app and give it a name
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

    def to_schema_dict(self):
        """
        return a simple represented dictionary in the format
        expected by the serializer MovieSchema
        """
        return {"id":self.id, "movie":self.movie ,"date":self.date}


class ShowtimeSchema(Schema):
    """ Defines how a Showtime instance will be serialized"""
    id = fields.String()
    movie = fields.Int()
    date = fields.Date()

    @post_load
    def make_showtime(self, data, **kwargs):
        return Showtime(**data)

# instantiate the schema serializer
showtimechema = ShowtimeSchema()
showtimeschema = ShowtimeSchema(many=True)

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
    """ Return all booking instances """
    showtimes = [showtime.to_schema_dict() for showtime in Showtime.query.all()]
    serialized_objects = showtimes_schema.dumps(showtimes, sort_keys=True, indent=4)

    return Response(
        response=serialized_objects,
        status=http_status.OK,
        mimetype="application/json"
    )


# add a route to GET showtimes for a certain date
@app.route("/showtimes/<date>", methods=['GET'])
def showtimes_record(date):
    date = date(*map(int, date_string.split('-')))
    query = Showtime.query.filter_by(date=date).all()

    if not query:
        raise NotFound

    showtimes = [result.to_schema_dict() for result in query]
    serialized_objects = showtimes_schema.dumps(showtimes, sort_keys=True, indent=4)

    return Response(
    response=serialized_objects,
    status=http_status.OK,
    mimetype="application/json"
    )
    
# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5002, debug=True)
