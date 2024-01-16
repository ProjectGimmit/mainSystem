import json
from flask import Flask, request
from modules.edit_json import read_config, write_config
from flask_cors import cross_origin

app = Flask(__name__)


#---------------
# アラーム一覧
#---------------
@app.route("/alarm")
@cross_origin(origins=["*"], methods=["GET"])
def get_alarms() :
	json_dist = read_config()
	alarm_list = {
		"mon": {
			"enable": json_dist["mon"]["enable"],
			"alarm": json_dist["mon"]["alarm"],
			"limit" : json_dist["mon"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["mon"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["mon"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["mon"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["mon"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["mon"]["gimmick"]["level"]["enable"],
			}
		},
		"tue": {
			"enable": json_dist["tue"]["enable"],
			"alarm": json_dist["tue"]["alarm"],
			"limit" : json_dist["tue"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["tue"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["tue"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["tue"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["tue"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["tue"]["gimmick"]["level"]["enable"],
			}
		},
		"wed": {
			"enable": json_dist["wed"]["enable"],
			"alarm": json_dist["wed"]["alarm"],
			"limit" : json_dist["wed"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["wed"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["wed"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["wed"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["wed"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["wed"]["gimmick"]["level"]["enable"],
			}
		},
		"thu": {
			"enable": json_dist["thu"]["enable"],
			"alarm": json_dist["thu"]["alarm"],
			"limit" : json_dist["thu"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["thu"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["thu"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["thu"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["thu"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["thu"]["gimmick"]["level"]["enable"],
			}
		},
		"fri": {
			"enable": json_dist["fri"]["enable"],
			"alarm": json_dist["fri"]["alarm"],
			"limit" : json_dist["fri"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["fri"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["fri"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["fri"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["fri"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["fri"]["gimmick"]["level"]["enable"],
			}
		},
		"sat": {
			"enable": json_dist["sat"]["enable"],
			"alarm": json_dist["sat"]["alarm"],
			"limit" : json_dist["sat"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["sat"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["sat"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["sat"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["sat"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["sat"]["gimmick"]["level"]["enable"],
			}
		},
		"sun": {
			"enable": json_dist["sun"]["enable"],
			"alarm": json_dist["sun"]["alarm"],
			"limit" : json_dist["sun"]["limit"],
			"gimmickEnable": {
				"wires": json_dist["sun"]["gimmick"]["wires"]["enable"],
				"toggleSW": json_dist["sun"]["gimmick"]["toggleSW"]["enable"],
				"keySW": json_dist["sun"]["gimmick"]["keySW"]["enable"],
				"lightsOut": json_dist["sun"]["gimmick"]["lightsOut"]["enable"],
				"level": json_dist["sun"]["gimmick"]["level"]["enable"],
			}
		}
	}
	return alarm_list

#------------------
# 設定用
#------------------
@app.route("/<weekday>", methods=["GET"])
@cross_origin(origins=["*"], methods=["GET"])
def read_mon(weekday) :
	# config.jsonの読み込み
	json_dist = read_config()
	return json_dist[weekday]

@app.route("/config/<weekday>", methods=["POST"])
@cross_origin(origins=["*"], methods=["POST"])
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
@cross_origin(origins=["*"], methods=["POST"])
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

#---------
# お試し実行
#---------
@app.route("/trial/<weekday>", methods=["GET"])
@cross_origin(origins=["*"], methods=["GET"])
def alarm_trial(weekday) :
	# アラームを取得
	json_dist = read_config()
	# weekdayのアラームを実行
	json_dist["trial"]["enable"] = True
	json_dist["trial"]["weekday"] = weekday
	write_config(json_dist)
	return json_dist[weekday]



if __name__ == "__main__" :
	app.run(port=8000, debug=True)