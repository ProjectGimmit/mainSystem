import json
import os

def read_json(json_path: str):
	print(json_path)
	with open(json_path, 'r') as f:
		json_dist = json.load(f)
	return json_dist

def write_json(json_path: str, writeItem):
		with open(json_path, "w") as f:
			json.dump(writeItem, f)

def read_config():
	# file_path = os.getcwd() + "/config.json"
	file_path = "/home/pi/Gimmit/mainSystem/config.json"
	with open(file_path, 'r') as f:
		json_dist = json.load(f)
	return json_dist

def write_config(writeItem):
	# file_path = os.getcwd() + "/config.json"
	file_path = "/home/pi/Gimmit/mainSystem/config.json"
	with open(file_path, "w") as f:
		json.dump(writeItem, f)