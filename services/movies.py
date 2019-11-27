from auxiliar import root_dir, nice_json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
import json


app = Flask(__name__)


# load the database
db_file = f"sqlite:///{root_dir()}/database/movies.db"
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


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "movies": "/movies",
            "movie": "/movies/<id>"
        }
    })

# route to get a movie by its id
@app.route("/movies/<movieid>", methods=['GET'])
def movie_info(movieid):
    if movieid not in movies:
        raise NotFound

    result = movies[movieid]
    result["uri"] = "/movies/{}".format(movieid)

    return nice_json(result)

# route to GET all movies
@app.route("/movies", methods=['GET'])
def movie_record():
    return nice_json(movies)

# exeuted when this is called from the cmd
if __name__ == "__main__":
    app.run(port=5001, debug=True)

