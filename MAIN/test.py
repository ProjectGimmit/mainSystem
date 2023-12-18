
import time
from multiprocessing import Process

def process_target() :
    print("in process")
    time.sleep(0.5)
    print("in process")
    time.sleep(0.5)
    print("in process")
    time.sleep(0.5)
    print("in process")
    time.sleep(0.5)
    print("in process")
    time.sleep(0.5)
    print("in process")
    time.sleep(0.5)

def hoge() :
  while True:
    while True:
      print("beep")
      time.sleep(3)
      break

    p = Process(target=process_target)
    p.start()

    while True:
      print("時間表示ループ")
      time.sleep(0.1)

      # プロセス（ギミック）が終了したら
      if not p.is_alive():
        print("プロセス終了")
        break
       
      # 時間超過
      # if timer_over :
      #
    
    if p.is_alive():
      print("再ループ")
      p.terminate()
    else :
      print("ループ終了")
      break
       
       

if __name__ == "__main__":
  print("start")
  hoge()
  print("end")