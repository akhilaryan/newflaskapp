from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask (__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)

lm = LoginManager()
lm.init_app(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'someone@example.com'
app.config["MAIL_PASSWORD"] = 'thepassword'

app.config['UPLOAD_FOLDER'] = '/Users/akhilaryan/developer/newflaskapp/app/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from routes import mail
mail.init_app(app)

