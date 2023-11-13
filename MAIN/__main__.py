# main.py

import datetime
import sys
import schedule
import os

from modules.edit_json import read_json, write_json

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.split(dir_path)[0] + "/config.json"

def hello():
	print("hello : ", datetime.datetime.now())

	json_content = read_json(file_path)
	print("json : ", json_content["test"]["content"])


def check_config() :
	print("check")
	json_dist = read_json(file_path)
	if json_dist["test"]["update"] :
		json_dist["test"]["update"] = False
		write_json(file_path, json_dist)		# ファイルへの書き込み
		scheduler1.clear("job")
		scheduler1.every(2).seconds.do(hello).tag("job")
	else :
		print("no update")

# schedulerの設定
def init_schedules(scheduler: schedule.Scheduler) :
	scheduler.clear()
	scheduler.every(1).seconds.do(hello).tag("job") # jobの登録
	scheduler.every(3).seconds.do(check_config).tag("check_json")


# schedulerクリア
def reset_scheduler(scheduler: schedule.Scheduler) :
	scheduler.clear()

# 初期設定
scheduler1 = schedule.Scheduler()
init_schedules(scheduler=scheduler1)


if __name__ == "__main__":
	try:
		while True:
			scheduler1.run_pending()
	except KeyboardInterrupt:
		sys.exit()

