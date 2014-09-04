import os
from intro_to_flask import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from forms import ContactForm, SignupForm
from flask.ext.mail import Message, Mail
from models import db
from flask_oauth import OAuth

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

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate()== False:
			return render_template('signup.html', form=form)
		else:
			return "[1] Create New User [2]Sign In the user [3] redirect to users profile"
	elif request.method == 'GET':
		return render_template ('signup.html', form=form)

# Facebook Authentication

FACEBOOK_APP_ID = '691001537654739'
FACEBOOK_APP_SECRET = '5db41d64579acb1840d8c3f26476c9ca'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)	

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))
		

		# Database Testing

""" @app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works'
	else:
		return 'Something is broken.' """