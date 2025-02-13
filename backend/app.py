from flask import Flask, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


mongoClient = MongoClient(
    'mongodb://admin:QWEASD123@192.168.101.15:27777/?authSource=admin')
db = mongoClient.get_database('names_db')
names_col = db.get_collection('names_col')


@app.route('/addname/<name>/')
def addname(name):
    names_col.insert_one({"name": name.lower()})
    return redirect(url_for('getnames'))


@app.route('/getnames/')
def getnames():
    names_json = []
    count = 0
    if names_col.find({}):
        for name in names_col.find({}).sort("name"):
            names_json.append({"name": name['name'], "id": str(name['_id'])})
            count += 1
            if count == 4:
                break
    return json.dumps(names_json)


if __name__ == "__main__":
    app.run(debug=True)
