from flask import Flask, render_template, jsonify


app = Flask(__name__)

@app.route('/home')
@app.route('/')
def return_index1():
    return render_template("index2.html")

@app.route('/about')
def return_index1():
    return render_template("index1.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
