import datetime
import random
import time
from toggleSW import ToggleSW
from keySW import KeySW
from level import Level
from lightsout import Lightsout
from modules.edit_json import read_config, write_config

LIMIT_TIME = 15 # ギミック解除タイムリミット(秒)

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
    main_scheduler.every(3).seconds.do(check_config).tag("check_json")
    main_scheduler.every(10).seconds.do(alarm_process, limit=LIMIT_TIME, weekday="mon")
    # config読み込み
    # 曜日ごとのスケジュール設定

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
    else:
        print("no update")



from mcp23017 import MCP23017
action_btn = MCP23017(0x27)
action_btn.GPIO_A_init(0xFF)

#---------------
# アラーム解除
#---------------
def alarm_process(limit: int, weekday: str):
    forced_stop = False # 強制停止フラグ
    while True:
        
        #-------------------
        # アラーム一時停止
        #-------------------
        while True:
            print("beep")
            time.sleep(3)
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
            tmp_time = limit - int(now_time - start_time)

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
            if not action_btn.GPIO_A_input(port=0) :
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
	toggleSW.stop()
	keySW.stop()
	level.stop()
	lightsout.stop()
	
	for value in enable_list :
		if value == "wires":
			print("wires")

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

	time.sleep(1)

	#---------------
	# ギミック停止
	#---------------
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
      toggleSW.stop()
      keySW.stop()
      level.stop()
      lightsout.stop()
      init_scheduler()
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
