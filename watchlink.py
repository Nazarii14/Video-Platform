from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.app_context().push()
app.config['SECRET_KEY'] = '2f23a88461aa5335f22200988f1ece8e1dcd731f58f1bb13e0dadd98b5485ad4'
# the following line means that database will be created in project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlink.db'
db = SQLAlchemy(app)


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
        flash(f'Logged in with account {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("sign in.html", title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)

