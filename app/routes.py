import os
from app import app, db, lm
from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory, g
from forms import ContactForm, SignupForm, SigninForm
from flask.ext.mail import Message, Mail
from flask.ext.login import current_user
from models import db, User
import facebook
from flask_oauth import OAuth
# from werkzeug import secure_filename

mail = Mail()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user=current_user
    if g.user.is_authenticated():
        db.session.add(g.user)
        db.session.commit()

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

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate()== False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('profile'))		

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signin.html', form = form)

@app.route('/signout')
def signout():
	if 'email' not in session:
		pop_login_session()
		return redirect(url_for('signin'))

	session.pop('email', None)
	pop_login_session()
	return redirect(url_for('home'))

# Facebook Authentication

FACEBOOK_APP_ID = '691001537654739'
FACEBOOK_APP_KEY = '5db41d64579acb1840d8c3f26476c9ca'

oauth = OAuth()

fb = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_KEY,
    request_token_params={'scope': ('email, ')}
)

@fb.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return fb.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@fb.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    
    elif 'email' not in session:
		fb_access_token = resp['access_token']

		graph = facebook.GraphAPI(fb_access_token)
		fb_details = graph.get_object('me')
		# fb_photo = graph.get_object('me/picture')
		# print fb_details

		firstname = fb_details['first_name']
		lastname = fb_details['last_name']
		email = fb_details['email']
		id = fb_details['id']
		# photo = fb_photo

		user = User(firstname, lastname, email, id)
		db.session.add(user)
		db.session.commit()
		# session['logged_in'] = True
		# session['facebook_token'] = (resp['access_token'], '')
		# return redirect(next_url)
		session['email'] = user.email
    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)

	# Profile
@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signup'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		user = g.user
		posts = [ #fake post
		{
			'author': {'firstname' : 'John'},
			'body' : 'Beautiful day'
		}
				]
		return render_template('profile.html',
			title = 'Profile',
			user = user,
			posts = posts)


		# Database Testing

""" @app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works'
	else:
		return 'Something is broken.' """

		# Uploads
# @app.route('/upload', methods=['POST'])
# def upload():
# 	file = request.files['file']
# 	if file and allowed_file(file.filename):
# 		filename = secure_filename(file.filename)
# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 		return redirect(url_for('uploaded_file', filename = filename))


# @app.route('/upload/<filename>')
# def uploaded_file(filename):
# 	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)