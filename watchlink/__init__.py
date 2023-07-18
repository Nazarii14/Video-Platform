from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.app_context().push()
app.config['SECRET_KEY'] = '2f23a88461aa5335f22200988f1ece8e1dcd731f58f1bb13e0dadd98b5485ad4'

# Database, the following line means that database will be created in project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlink.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # <-- function name of route
login_manager.login_message_category = 'info'

from watchlink import routes
