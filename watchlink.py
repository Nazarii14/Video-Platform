from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from forms import RegistrationForm, LoginForm


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.app_context().push()
app.config['SECRET_KEY'] = '2f23a88461aa5335f22200988f1ece8e1dcd731f58f1bb13e0dadd98b5485ad4'

# Database, the following line means that database will be created in project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlink.db'
db = SQLAlchemy(app)

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


@app.route("/")
@app.route("/home")
def home():
    email = dict(session)['profile']['email']
    return f'Hello, you are logged in as {email}!'
#    return render_template("home.html", videos=simple_data)


@app.route("/about")
def about():
    return render_template("about.html")


# register account in watchlink
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("sign up.html", title='Register', form=form)


# native app login
@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in with account {form.email.data}!', 'success')
        return redirect(url_for('home'))
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
    return redirect('/')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
