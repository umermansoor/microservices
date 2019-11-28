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

# instantiate a flask app and give it a name
app = Flask(__name__)

# load the database
root_dir = dirname(realpath(__file__ + '/..'))
db_file = f"sqlite:///{root_dir}/database/rewards.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Reward(db.Model):
    """ This class maps the database reward model """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Reward: {self.user} has {self.score} points>"

    def to_schema_dict(self):
        """
        return a simple represented dictionary in the format
        expected by the serializer RewardSchema
        """
        return { "id":self.id, "user":self.user ,"score":self.score }


class RewardSchema(Schema):
    """ Defines how a Reward instance will be serialized"""
    id = fields.String()
    user = fields.Int()
    score = fields.Int()

    @post_load
    def make_reward(self, data, **kwargs):
        return Reward(**data)

# instantiate the schema serializer
reward_schema = RewardSchema()
rewards_schema = RewardSchema(many=True)


# Route for adding a new score
@app.route("/rewards/new_score", methods=["POST"])
def new_movie():
    """ Make a new score after a POST request """
    json_repsonse = request.get_json()
    user = int(json_repsonse.get('user'))
    score = int(json_repsonse.get('score'))
    user_score = Reward.query.filter_by(user=user).first_or_404()
    user_score.score += score
    # save data:
    db.session.commit()

    return Response(
      response=movie_schema.dumps(new_movie.to_schema_dict(), sort_keys=True, indent=4),
      status=http_status.OK,
      mimetype='application/json'
   )


if __name__ == '__main__':
	app.run(port=5004, debug=True)
