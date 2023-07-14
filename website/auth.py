from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route("/")
def hello():
    return "<h1>hello</h1>"
