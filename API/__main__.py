import json
from flask import Flask, request
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

#---------
# 月曜日
#---------
@app.route("/mon", methods=["GET"])
def read_mon() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["mon"]

@app.route("/mon", methods=["POST"])
def update_mon() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["mon"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "UPDATE MONDAY"


#---------
# 火曜日
#---------
@app.route("/tue")
def read_tue() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["tue"]

@app.route("/tue", methods=["POST"])
def update_tue() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["tue"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE TUESDAY</p>"

#---------
# 水曜日
#---------
@app.route("/wed")
def read_wed() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["wed"]

@app.route("/wed", methods=["POST"])
def update_wed() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["wed"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE WEDNESDAY</p>"

#---------
# 木曜日
#---------
@app.route("/thu")
def read_thu() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["thu"]

@app.route("/thu", methods=["POST"])
def update_thu() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["thu"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE THURSDAY</p>"

#---------
# 金曜日
#---------
@app.route("/fri")
def read_fri() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["fri"]

@app.route("/fri", methods=["POST"])
def update_fri() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["fri"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE FRIDAY</p>"

#---------
# 土曜日
#---------
@app.route("/sat")
def read_sat() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["sat"]

@app.route("/sat", methods=["POST"])
def update_sat() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["sat"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE SATADAY</p>"

#---------
# 日曜日
#---------
@app.route("/sun")
def read_sun() :
	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)
	return json_dist["sun"]

@app.route("/sun", methods=["POST"])
def update_sun() :
	# リクエストボディの取得
	data = request.get_json()

	# config.jsonの読み込み
	json_dist = read_json(json_path=file_path)

	json_dist["sun"] = data
	json_dist["update"] = True
	write_json(file_path, json_dist)		# ファイルへの書き込み

	return "<p>UPDATE WEDNESDAY</p>"


if __name__ == "__main__" :
	app.run(port=8000)

"""
curl -X POST -H "Content-Type: application/json" -d '{
	"enable": false,
  "alarm": "0900",
  "gimmick": {
    "wires": {
      "enable": false,
      "answer": [true, true, true, true]
    },
    "toggleSW": {
      "enable": false,
      "answer": [true, true, true, true, true]
    },
    "keySW": {
      "enable": false,
			"pattern":[true,false],
      "default": [true, true, true]
    },
    "lightsOut": {
      "enable": true,
      "default": [false, true, false, true, false, true, false, true, false]
    },
    "level": {
      "enable": true,
      "answer": 10
    }
  }
}' localhost:8000/tue


curl localhost:8000/tue
"""