from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField

class ContactForm(Form):
	name = TextField("Name")
	email = TextField("Email ID")
	subject = TextField("Subject")
	message = TextAreaField("How can I help?")
	submit = SubmitField("Send")