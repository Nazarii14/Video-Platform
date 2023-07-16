from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, session, abort, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth


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

CLIENT_ID_FACEBOOK = 294032019865535
CLIENT_SECRET_FACEBOOK = "9228e7da8d1cc3097ae9f9664d5ee22f"


facebook = oauth.register(
    'facebook',
    consumer_key=CLIENT_ID_FACEBOOK,
    consumer_secret=CLIENT_SECRET_FACEBOOK,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth'
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    videos = db.relationship('Video', backref='author', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Video ('{self.title}', '{self.date_posted}', '{self.image_file}')"


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


# to do
@app.route("/facebook_login")
def facebook_login():
    return redirect(url_for('facebook_authorized', callback=url_for('facebook_authorized', _external=True)))


# to do
@app.route('/facebook-authorized')
def facebook_authorized():
    response = facebook.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['facebook_token'] = (response['access_token'], '')

    return redirect(url_for('/'))


if __name__ == "__main__":
    app.run(debug=True)
