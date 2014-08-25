from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators

class ContactForm(Form):
	name = TextField("Name", [validators.Required("Please enter your Name")])
	email = TextField("Email ID", [validators.Required("Please enter a valid Email ID"), validators.Email()])
	subject = TextField("Subject", [validators.Required("Please enter a Subject for your Message")])
	message = TextAreaField("How can I help?", [validators.Required("Please enter your message for us.")])
	submit = SubmitField("Send")