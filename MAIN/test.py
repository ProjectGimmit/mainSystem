import time
from multiprocessing import Process
import RPi.GPIO as GPIO

ALARM_BTN = 5
FORCE_BTN = 6

BUZZER = 13

GPIO.setmode(GPIO.BCM) 
GPIO.setup(BUZZER,GPIO.OUT,initial=GPIO.LOW)
p = GPIO.PWM(BUZZER,100)
GPIO.setup(ALARM_BTN,GPIO.IN)
GPIO.setup(FORCE_BTN,GPIO.IN)

if __name__ == "__main__":

  print("start")
  try :
    p.ChangeFrequency(1000)
    while True :
    #   alarmBtn = GPIO.input(ALARM_BTN)
    #   forceBtn = GPIO.input(FORCE_BTN)
    #   if not alarmBtn :
    #     print("alarm")
    #   if not forceBtn :
    #     print("force")
      p.start(95) 
      time.sleep(0.1)
      p.stop()
      time.sleep(0.1)

      p.start(95) 
      time.sleep(0.1)
      p.stop()
      time.sleep(0.1)

      p.start(95) 
      time.sleep(0.1)
      p.stop()
      time.sleep(1)



  except  KeyboardInterrupt:
    GPIO.cleanup()
  print("end")