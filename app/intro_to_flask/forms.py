from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, PasswordField

class ContactForm(Form):
	name = TextField("Name", [validators.Required("Please enter your Name")])
	email = TextField("Email ID", [validators.Required("Please enter a valid Email ID"), validators.Email()])
	subject = TextField("Subject", [validators.Required("Please enter a Subject for your Message")])
	message = TextAreaField("How can I help?", [validators.Required("Please enter your message for us.")])
	submit = SubmitField("Send")

class SignupForm(Form):
	firstname = TextField("First Name", [validators.Required("Please enter your first name")])
	lastname = TextField("Last Name", [validators.Required("Please ented your last name")])
	email = TextField("Email", [validators.Required("Please enter a valid email address"), validators.Email("PLease enter a valid email address")])
	password = PasswordField("Password", [validators.Required("Please enter a password.")])
	submit = SubmitField("Create Account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email=self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken.")
			return False
		else:
			return True