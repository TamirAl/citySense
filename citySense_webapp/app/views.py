import time
from flask import render_template,Response, flash, redirect, url_for, request, abort,jsonify,stream_with_context,make_response
from app import *
import pymongo

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/get_last_item_sensor/<sensor_id>',methods = ['GET','POST'])
def get_last_item_sensor(sensor_id):
	cursor = environment_collection.find({"sensor_id": sensor_id}, {"_id": False}).sort("timestamp", pymongo.DESCENDING).limit(1)
	cursor_records = list(cursor)[0]
	
	return jsonify(cursor_records)