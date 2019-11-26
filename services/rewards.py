from services import root_dir
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# load the database
db_file = f"sqlite:///{root_dir()}/database/rewards.db"
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


if __name__ == '__main__':
	app.run(port=5004, debug=True)
