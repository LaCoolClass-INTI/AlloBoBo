from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config["SECRET_KEY"] = "ebb568971db8c0cd2f830a55010f5ac04cb6149b"
app.config["MONGO_URI"] = "mongodb+srv://alloboboConnect:allobobo@cluster0.bs4uh.mongodb.net/allobobo?ssl=true&ssl_cert_reqs=CERT_NONE"
app.config.from_object(Config)
mail = Mail(app)
# Setup MongoDB

mongodb_client = PyMongo(app)
db = mongodb_client.db

from application import routes