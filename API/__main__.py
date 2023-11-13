import json
from flask import Flask
import os
from modules.edit_json import read_json, write_json

app = Flask(__name__)

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.split(dir_path)[0] + "/config.json"

@app.route("/config")
def hello_world() :
	json_dist = read_json(json_path=file_path)
	print(json_dist)
	return "<p>Hello, World!</p>"

##########
# 月曜日 #
##########
@app.route("/mon")
def read_mon() :
	return "<p>READ MONDAY</p>"

@app.route("/mon", methods=["POST"])
def update_mon() :
	# jsonの読み込み
	json_dist = read_json(json_path=file_path)
	json_dist["test"]["content"] = True	# データの追加・変更
	json_dist["test"]["update"] = True	# データの追加・変更
	write_json(file_path, json_dist)		# ファイルへの書き込み
	return "UPDATE MONDAY"


##########
# 火曜日 #
##########
@app.route("/tue")
def read_tue() :
	return "<p>READ MONDAY</p>"

@app.route("/tue", methods=["POST"])
def update_tue() :
	# jsonの読み込み
	json_dist = read_json(json_path=file_path)
	json_dist["test"]["content"] = False	# データの追加・変更
	json_dist["test"]["update"] = True	# データの追加・変更
	write_json(file_path, json_dist)		# ファイルへの書き込み
	return "<p>UPDATE TUESDAY</p>"

##########
# 水曜日 #
##########
@app.route("/wed")
def read_wed() :
	return "<p>READ WEDNESDAY</p>"

@app.route("/wed", methods=["POST"])
def update_wed() :
	return "<p>UPDATE WEDNESDAY</p>"

##########
# 木曜日 #
##########
@app.route("/thu")
def read_thu() :
	return "<p>READ THURSDAY</p>"

@app.route("/thu", methods=["POST"])
def update_thu() :
	return "<p>UPDATE THURSDAY</p>"

##########
# 金曜日 #
##########
@app.route("/fri")
def read_fri() :
	return "<p>READ FRIDAY</p>"

@app.route("/fri", methods=["POST"])
def update_fri() :
	return "<p>UPDATE FRIDAY</p>"

##########
# 土曜日 #
##########
@app.route("/sat")
def read_sat() :
	return "<p>READ SATADAY</p>"

@app.route("/sat", methods=["POST"])
def update_sat() :
	return "<p>UPDATE SATADAY</p>"

##########
# 日曜日 #
##########
@app.route("/sun")
def read_sun() :
	return "<p>READ SUNDAY</p>"

@app.route("/sun", methods=["POST"])
def update_sun() :
	return "<p>UPDATE WEDNESDAY</p>"


if __name__ == "__main__" :
	app.run(port=8000)
