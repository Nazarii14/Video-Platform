from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return "<h1>Home</h1>"
    #return render_template("home.html")
