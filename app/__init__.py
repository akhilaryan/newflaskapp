from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'someone@example.com'
app.config["MAIL_PASSWORD"] = 'thepassword'

from routes import mail
mail.init_app(app)

# from models import db
db.init_app(app)