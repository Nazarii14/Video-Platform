import os.path
import pathlib
from datetime import datetime
import google.auth.transport.requests
from flask import Flask, render_template, url_for, flash, redirect, session, abort, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from google_auth_oauthlib.flow import Flow
import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import google.oauth2.credentials

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.app_context().push()
app.config['SECRET_KEY'] = '2f23a88461aa5335f22200988f1ece8e1dcd731f58f1bb13e0dadd98b5485ad4'

# the following line means that database will be created in project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlink.db'

db = SQLAlchemy(app)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "403190142187-8nr76rl9fu4veafi9gj8dct1s1thjb9g.apps.googleusercontent.com"
client_secret_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
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

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authentification required
        else:
            return function()

    return wrapper


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", videos=simple_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("sign up.html", title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in with account {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("sign in.html", title='Login', form=form)



@app.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match

    credentials = flow.credentials
    request_session = request.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Store the necessary user information in the session or database as needed
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    return redirect("/protected_area")



@app.route("/google_logout")
def google_logout():
    session.clear()
    return redirect("/")


@app.route("/facebook_login")
def facebook_login():
    pass


@app.route("/linkedin_login")
def linkedin_login():
    pass



@app.route("/protected_area")
@login_is_required
def protected_area():
    return "Protected!"


if __name__ == "__main__":
    app.run(debug=True)
