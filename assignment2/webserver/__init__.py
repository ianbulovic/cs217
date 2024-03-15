from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "73d833853a26382c1ccdd8b9bd6642d3"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_ner.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from webserver import routes
