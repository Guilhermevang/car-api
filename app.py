import flask
from flask import request, jsonify
import json
import db

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/cars', methods=['GET'])
def Cars():
  data = db.FindAll()
  return jsonify(data)

@app.route('/cars/<key>/<value>', methods=['GET'])
def CarsFilter(key, value):
  data = db.FindAll(key, value, 5)
  return jsonify(data)

@app.route('/car/<id>', methods=['GET'])
def Car(id):
  data = db.Find('id', id)
  return jsonify(data)

app.run()