import json
from flask import Flask, request
from modules.edit_json import read_config, write_config
from flask_cors import cross_origin

app = Flask(__name__)


#---------------
# アラーム一覧
#---------------
@app.route("/alarm")
@cross_origin(origins=["http://localhost:5173"], methods=["GET"])
def get_alarms() :
	json_dist = read_config()
	alarm_list = {
		"mon": {
			"enable": json_dist["mon"]["enable"],
			"alarm": json_dist["mon"]["alarm"],
		},
		"tue": {
			"enable": json_dist["tue"]["enable"],
			"alarm": json_dist["tue"]["alarm"],
		},
		"wed": {
			"enable": json_dist["wed"]["enable"],
			"alarm": json_dist["wed"]["alarm"],
		},
		"thu": {
			"enable": json_dist["thu"]["enable"],
			"alarm": json_dist["thu"]["alarm"],
		},
		"fri": {
			"enable": json_dist["fri"]["enable"],
			"alarm": json_dist["fri"]["alarm"],
		},
		"sat": {
			"enable": json_dist["sat"]["enable"],
			"alarm": json_dist["sat"]["alarm"],
		},
		"sun": {
			"enable": json_dist["sun"]["enable"],
			"alarm": json_dist["sun"]["alarm"],
		}
	}
	return alarm_list

#---------
# 月曜日
#---------
@app.route("/<weekday>", methods=["GET"])
@cross_origin(origins=["http://localhost:5173"], methods=["GET"])
def read_mon(weekday) :
	# config.jsonの読み込み
	json_dist = read_config()
	return json_dist[weekday]

@app.route("/config/<weekday>", methods=["POST"])
@cross_origin(origins=["http://localhost:5173"], methods=["POST"])
def update_mon(weekday) :
	# リクエストボディの取得
	data = request.get_json()
	# config.jsonの読み込み
	json_dist = read_config()
	json_dist[weekday] = data
	json_dist["update"] = True
	write_config(json_dist)
	return "UPDATE MONDAY"

@app.route("/alarm/<weekday>", methods=["POST"])
@cross_origin(origins=["http://localhost:5173"], methods=["POST"])
def update_mon_alarm(weekday) :
	# リクエストボディの取得
	data = request.get_json()
	# config.jsonの読み込み
	json_dist = read_config()
	json_dist[weekday]["enable"] = data["enable"]
	json_dist[weekday]["alarm"] = data["alarm"]
	json_dist["update"] = True
	write_config(json_dist)
	return "UPDATE MONDAY"



# #---------
# # 火曜日
# #---------
# @app.route("/tue")
# def read_tue() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["tue"]

# @app.route("/tue", methods=["POST"])
# def update_tue() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["tue"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE TUESDAY</p>"


# #---------
# # 水曜日
# #---------
# @app.route("/wed")
# def read_wed() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["wed"]

# @app.route("/wed", methods=["POST"])
# def update_wed() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["wed"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE WEDNESDAY</p>"


# #---------
# # 木曜日
# #---------
# @app.route("/thu")
# def read_thu() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["thu"]

# @app.route("/thu", methods=["POST"])
# def update_thu() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["thu"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE THURSDAY</p>"


# #---------
# # 金曜日
# #---------
# @app.route("/fri")
# def read_fri() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["fri"]

# @app.route("/fri", methods=["POST"])
# def update_fri() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["fri"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE FRIDAY</p>"


# #---------
# # 土曜日
# #---------
# @app.route("/sat")
# def read_sat() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["sat"]

# @app.route("/sat", methods=["POST"])
# def update_sat() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["sat"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE SATADAY</p>"


# #---------
# # 日曜日
# #---------
# @app.route("/sun")
# def read_sun() :
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	return json_dist["sun"]

# @app.route("/sun", methods=["POST"])
# def update_sun() :
# 	# リクエストボディの取得
# 	data = request.get_json()
# 	# config.jsonの読み込み
# 	json_dist = read_config()
# 	json_dist["sun"] = data
# 	json_dist["update"] = True
# 	write_config(json_dist)
# 	return "<p>UPDATE WEDNESDAY</p>"


if __name__ == "__main__" :
	app.run(port=8000, debug=True)

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
}' localhost:8000/alarm/mon

curl -X POST -H "Content-Type: application/json" -d '{"enable": true, "alarm": "1330" }' localhost:8000/alarm/mon

curl localhost:8000/tue
"""