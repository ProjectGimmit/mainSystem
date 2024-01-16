import datetime
import random
import time

from wires import Wires
from toggleSW import ToggleSW
from keySW import KeySW
from level import Level
from lightsout import Lightsout
from modules.edit_json import read_config, write_config

LIMIT_TIME = 60 # ギミック解除タイムリミット(秒)

# #-----------
# # toggleSW
# #-----------
wires = Wires()

# #-----------
# # toggleSW
# #-----------
toggleSW = ToggleSW()

# #-----------
# # keySW
# #-----------
keySW = KeySW()

# #-----------
# # level
# #-----------
level = Level()

# #-----------
# # lightsout
# #-----------
lightsout = Lightsout()


import schedule as main_scheduler
from multiprocessing import Process
import tm1637

tm = tm1637.TM1637(clk=21, dio=20)

#-----------------------
# スケジューラ初期設定
#-----------------------
def init_scheduler():
    main_scheduler.clear()
    main_scheduler.every(1).seconds.do(check_config).tag("check_json")
    # main_scheduler.every(10).seconds.do(alarm_process, limit=LIMIT_TIME, weekday="mon")
    # config読み込み
    config = read_config()
    # 曜日ごとのスケジュール設定
    if config["mon"]["enable"] :
         alarm_tmp = config["mon"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().monday.at(alarm_str).do(alarm_process, weekday="mon")
    if config["tue"]["enable"] :
         alarm_tmp = config["tue"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().tuesday.at(alarm_str).do(alarm_process, weekday="tue")
    if config["wed"]["enable"] :
         alarm_tmp = config["wed"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().wednesday.at(alarm_str).do(alarm_process, weekday="wed")
    if config["thu"]["enable"] :
         alarm_tmp = config["thu"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().thursday.at(alarm_str).do(alarm_process, weekday="thu")
    if config["fri"]["enable"] :
         alarm_tmp = config["fri"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().friday.at(alarm_str).do(alarm_process, weekday="fri")
    if config["sat"]["enable"] :
         alarm_tmp = config["sat"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().saturday.at(alarm_str).do(alarm_process, weekday="sat")
    if config["sun"]["enable"] :
         alarm_tmp = config["sun"]["alarm"]
         alarm_str = alarm_tmp[:2] + ":" + alarm_tmp[2:]
         main_scheduler.every().sunday.at(alarm_str).do(alarm_process, weekday="sun")

#-------------------------
# 設定ファイルの更新確認
#-------------------------
def check_config():
    # print("check")
    config = read_config()
    if config["update"]:
        init_scheduler()
        config["update"] = False
        write_config(config)
    
    if config["trial"]["enable"]:
        main_scheduler.clear()
        config["trial"]["enable"] = False
        write_config(config)
        alarm_process(weekday=config["trial"]["weekday"])
        init_scheduler()



import RPi.GPIO as GPIO

ALARM_BTN = 5
FORCE_BTN = 6
BUZZER = 13

GPIO.setmode(GPIO.BCM) 
GPIO.setup(ALARM_BTN,GPIO.IN)
GPIO.setup(FORCE_BTN,GPIO.IN)
GPIO.setup(BUZZER,GPIO.OUT,initial=GPIO.LOW)
buzzer = GPIO.PWM(BUZZER,100)

def alarm():
    buzzer.ChangeFrequency(1000)
    while True :
      buzzer.start(95) 
      time.sleep(0.1)
      buzzer.stop()
      time.sleep(0.1)

      buzzer.start(95) 
      time.sleep(0.1)
      buzzer.stop()
      time.sleep(0.1)

      buzzer.start(95) 
      time.sleep(0.1)
      buzzer.stop()
      time.sleep(1)
     

#---------------
# アラーム解除
#---------------
def alarm_process(weekday: str):
    # タイムリミット取得
    CONFIG = read_config()
    LIMIT_CONFIG = CONFIG[weekday]["limit"]

    forced_stop = False # 強制停止フラグ
    while True:
        
        #-------------------
        # アラーム一時停止
        #-------------------
        p = Process(target=alarm)
        p.start()
        while True:
            if not GPIO.input(ALARM_BTN) : 
                p.terminate()
                break

        #------------------
        # ギミック解除プロセス開始
        #------------------
        p = Process(target=main_process, kwargs={'weekday': weekday})
        p.start()

        #-----------------------
        # タイムリミット用変数
        #-----------------------
        start_time = time.monotonic()
        view_time = 0

        #-------------
        # 解除ループ
        #-------------
        while True:
            #-----------------
            # カウントダウン
            #-----------------
            now_time = time.monotonic()
            tmp_time = LIMIT_CONFIG - int(now_time - start_time)

            if view_time != tmp_time:
              view_time = tmp_time
              tm.number(tmp_time)

            #-----------
            # 時間超過
            #-----------
            if tmp_time == 0:
              break
            #-----------------------------------
            # プロセス（ギミック）が終了したら
            #-----------------------------------
            if not p.is_alive():
                print("プロセス終了")
                break
            #-----------
            # 強制停止
            #-----------
            if not GPIO.input(FORCE_BTN) :
              forced_stop = True
              break

        #----------------
        # 終了 or 再ループ
        #----------------
        if forced_stop:
            print("強制停止")
            p.terminate()
            break
        elif p.is_alive():
            print("再ループ")
            p.terminate()
        else:
            print("ループ終了")
            break
    
    toggleSW.stop()
    keySW.stop()
    level.stop()
    lightsout.stop()
    wires.stop()
    h, m = clock()
    tm.numbers(h, m, colon=True)


#-----------
# ギミック
#-----------
def main_process(weekday) :
	CONFIG = read_config()
	MON_CONFIG = CONFIG[weekday]
	WIRES_CONFIG 		 = MON_CONFIG["gimmick"]["wires"]
	TOGGLE_SW_CONFIG = MON_CONFIG["gimmick"]["toggleSW"]
	KEY_SW_CONFIG 	 = MON_CONFIG["gimmick"]["keySW"]
	LIGHTSOUT_CONFIG = MON_CONFIG["gimmick"]["lightsOut"]
	LEVEL_CONFIG 		 = MON_CONFIG["gimmick"]["level"]

	config = read_config()[weekday]
	gimmick_list = config['gimmick']
	enable_list = []
	for key, value in gimmick_list.items():
		if value["enable"] :
			enable_list.append(key)
	random.shuffle(enable_list)

	#-------------------
	# ギミックリセット
	#-------------------
	wires.stop()
	toggleSW.stop()
	keySW.stop()
	level.stop()
	lightsout.stop()
	
	for value in enable_list :
		if value == "wires":
			wires.loop(WIRES_CONFIG)

		if value == "toggleSW":
			print("toggleSW")
			toggleSW.loop(TOGGLE_SW_CONFIG)

		if value == "keySW":
			print("keySW")
			keySW.loop(KEY_SW_CONFIG)

		if value == "lightsOut":
			print("lightsOut")
			lightsout.loop(LIGHTSOUT_CONFIG)

		if value == "level":
			print("level")
			level.loop(LEVEL_CONFIG)

	while True:
		if not GPIO.input(ALARM_BTN) : break

	#---------------
	# ギミック停止
	#---------------
	wires.stop()
	toggleSW.stop()
	keySW.stop()
	level.stop()
	lightsout.stop()

#---------------
# 現在時刻取得
#---------------
def clock() -> int:
  now_time = datetime.datetime.now()
  h = now_time.strftime("%H")
  m = now_time.strftime("%M")
  return int(h), int(m)


#---------------
# メインループ
#---------------
if __name__ == "__main__":
    try:
      init_scheduler()
      wires.stop()
      toggleSW.stop()
      keySW.stop()
      level.stop()
      lightsout.stop()
      view_h = 0
      view_m = 0
      while True:
        main_scheduler.run_pending()
          
        h, m = clock()
        if view_m != m:
          view_h = h
          view_m = m
          tm.numbers(h, m, colon=True)


    except KeyboardInterrupt:
      print("end")
