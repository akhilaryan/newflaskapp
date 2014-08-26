from intro_to_flask import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import ContactForm
from flask.ext.mail import Message, Mail
from models import db

mail = Mail()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash ('All fields are required')
			return render_template ('contact.html', form=form)
		else:
			msg = Message(form.subject.data, sender='someone@example.com', recipients=['your@youremail.com'])
			msg.body = """
			%s <%s>
			%s
			""" %(form.subject.data, form.email.data, form.message.data)
			mail.send(msg)

			return render_template('contact.html', success=True)

	elif request.method == 'GET':
		return render_template('contact.html', form=form)

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works'
	else:
		return 'Something is broken.'