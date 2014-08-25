from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators

class ContactForm(Form):
	name = TextField("Name", [validators.Required()])
	email = TextField("Email ID", [validators.Required(), validators.Email()])
	subject = TextField("Subject", [validators.Required()])
	message = TextAreaField("How can I help?", [validators.Required()])
	submit = SubmitField("Send")