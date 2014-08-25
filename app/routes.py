from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask.ext.mail import Message, Mail

mail = Mail()

app = Flask (__name__)

app.secret_key = "somekey"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'someone@example.com'
app.config["MAIL_PASSWORD"] = 'thepassword'
 
mail.init_app(app)

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

if __name__ == '__main__':
	app.run(debug=True)