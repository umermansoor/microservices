from services import root_dir
from flask import Flask, json, jsonify
from werkzeug.exceptions import NotFound


app = Flask(__name__)

with open("{}/database/movies.json".format(root_dir()), 'r') as f:
    movies = json.load(f)

@app.route("/")
def hello():
    return jsonify({
        'uri': "/",
        'subresource_uris': {
            'movies': '/movies',
            'movie': '/movies</id>'
        }
    })

@app.route("/movies/<movieid>")
def movie_info(movieid):
    if movieid not in movies:
        raise NotFound

    return jsonify(movies[movieid])

@app.route("/movies")
def movie_list():
    return jsonify(movies)




if __name__ == "__main__":
    app.run(port=5001, debug = True)

