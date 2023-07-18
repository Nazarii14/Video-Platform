from authlib.integrations.flask_client import OAuth
from watchlink.models import User, Video
from watchlink import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, session, abort, request
from watchlink.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='1028720449984-bulqio8hbjc4mej8910g9oi1tlk93hn5.apps.googleusercontent.com',
    client_secret='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',
    authorize_params={
        'scope': 'openid email profile',
        'access_type': 'offline'
    },
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header'
    },
    issuer='https://accounts.google.com'
)


simple_data = [
    {
        'videoName': 'name1',
        'videoLength': '1:01',
        'channelName': 'volodia228',
        'datePosted': 'May 20, 2023'
    }, {
        'videoName': 'name2',
        'videoLength': '1:31',
        'channelName': 'volodia228',
        'datePosted': 'June 10, 2023'
    }, {
        'videoName': 'name3',
        'videoLength': '3:52',
        'channelName': 'volodia228',
        'datePosted': 'July 07, 2023'
    }
]


@app.route("/testing_google_login")
def testing_google_login():
    email = dict(session)['profile']['email']
    return f'Hello, you are logged in as {email}!'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", videos=simple_data)

@app.route("/about")
def about():
    return render_template("about.html")


# register account in watchlink
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        #hashing password, creating user and adding to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created for {form.username.data}! Encrypted password: {hashed_password}', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


# native app login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'success')
    return render_template("sign in.html", title='Login', form=form)


# google login
@app.route('/google_login')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def google_authorize():
    google = oauth.create_client('google')
    try:
        token = google.authorize_access_token()
    except Exception as e:
        print("Error obtaining access token:", e)

    resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    session['profile'] = user_info
    session.permanent = True
    return redirect('/testing_google_login')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title='Account')

