from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# from pymongo import MongoClient
#
# app = Flask(__name__)
#
# client = MongoClient("mongodb://localhost:@localhost:27017/video")
# db = client.database
#

#
#
# @app.route('/about')
# def return_index2():
#     return render_template("about.html")
#
#
# @app.route('/data', methods=['GET'])
# def get_data():
#     collection = db.my_collection
#     data = list(collection.find())
#     return jsonify(data)



