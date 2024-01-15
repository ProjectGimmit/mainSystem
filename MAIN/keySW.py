import os
import random
import time
from mcp23017 import MCP23017

from modules.edit_json import read_config


class KeySW:
    def __init__(self) -> None:
        self.keySW_main = MCP23017(0x22)
        self.keySW_main.GPIO_A_init(0xFF)  # 入力
        self.keySW_main.GPIO_B_init(0x00)  # 出力
    
    #-----------
    # 初期設定
    #-----------
    def __init_gimmick(self, keySW_config: any):

        default = keySW_config["default"]
        self.keySW_main.GPIO_B_output(port=0, on=1 if default[0] else 0)
        self.keySW_main.GPIO_B_output(port=1, on=1 if default[1] else 0)
        self.keySW_main.GPIO_B_output(port=2, on=1 if default[2] else 0)

        self.pattern_num = 0
        pattern = keySW_config["pattern"]
        self.keySW_main.GPIO_B_output(port=3, on=0)
        self.keySW_main.GPIO_B_output(port=4, on=0)

        if pattern[0] :
            self.pattern_num += 2
            self.keySW_main.GPIO_B_output(port=3, on=1)

        if pattern[1] :
            self.pattern_num += 1
            self.keySW_main.GPIO_B_output(port=4, on=1)
        
        print(self.pattern_num)
    

    #-----------
    # 左を点灯
    #-----------
    def __on_left(self):
        self.keySW_main.GPIO_B_output(port=0, on=1)

    #-----------
    # 右を消灯
    #-----------
    def __off_right(self):
        self.keySW_main.GPIO_B_output(port=2, on=0)

    #-----------
    # 反転
    #-----------
    def __switching_lights(self):
      left_light   = self.keySW_main.GPIO_B_input(port=0)
      center_light = self.keySW_main.GPIO_B_input(port=1)
      right_light  = self.keySW_main.GPIO_B_input(port=2)

      if left_light :
          self.keySW_main.GPIO_B_output(port=0, on=0)
      else :
          self.keySW_main.GPIO_B_output(port=0, on=1)
        
      if center_light :
          self.keySW_main.GPIO_B_output(port=1, on=0)
      else :
          self.keySW_main.GPIO_B_output(port=1, on=1)

      if right_light :
          self.keySW_main.GPIO_B_output(port=2, on=0)
      else :
          self.keySW_main.GPIO_B_output(port=2, on=1)

    #-----------c
    # left_key
    #-----------
    def __left_key(self):
        if self.pattern_num == 0 :
            self.__on_left()
        if self.pattern_num == 1 :
            self.__switching_lights()
        if self.pattern_num == 2 :
            self.__on_left()
        if self.pattern_num == 3 :
            self.__off_right()

    #-----------
    # center_key
    #-----------
    def __center_key(self):
        if self.pattern_num == 0 :
            self.__switching_lights()
        if self.pattern_num == 1 :
            self.__on_left()
        if self.pattern_num == 2 :
            self.__off_right()
        if self.pattern_num == 3 :
            self.__switching_lights()

    #-----------
    # right_key
    #-----------
    def __right_key(self):
        if self.pattern_num == 0 :
            self.__off_right()
        if self.pattern_num == 1 :
            self.__off_right()
        if self.pattern_num == 2 :
            self.__switching_lights()
        if self.pattern_num == 3 :
            self.__on_left()

    #-------------
    # スタンバイ
    #-------------
    def standby(self):
        self.keySW_main.GPIO_B_output(port=5, on=0)
        self.keySW_main.GPIO_B_output(port=6, on=1)

    #-------
    # 停止
    #-------
    def stop(self):
        self.keySW_main.GPIO_B_output(port=0, on=0)
        self.keySW_main.GPIO_B_output(port=1, on=0)
        self.keySW_main.GPIO_B_output(port=2, on=0)
        self.keySW_main.GPIO_B_output(port=3, on=0)
        self.keySW_main.GPIO_B_output(port=4, on=0)
        self.keySW_main.GPIO_B_output(port=5, on=0)
        self.keySW_main.GPIO_B_output(port=6, on=0)

    #---------
    # メイン
    #---------
    def loop(self,  keySW_config: any):
        left_key_flg   = False
        center_key_flg = False
        right_key_flg  = False

        if self.keySW_main.GPIO_A_input(port=2):
            left_key_flg   = True

        if self.keySW_main.GPIO_A_input(port=1):
            center_key_flg = True

        if self.keySW_main.GPIO_A_input(port=0):
            right_key_flg  = True

        self.__init_gimmick(keySW_config)
        self.keySW_main.GPIO_B_output(port=5, on=0)
        self.keySW_main.GPIO_B_output(port=6, on=1)

        while True:
            left_key = self.keySW_main.GPIO_A_input(port=2)
            center_key = self.keySW_main.GPIO_A_input(port=1)
            right_key = self.keySW_main.GPIO_A_input(port=0)

            if not left_key and left_key_flg :
                self.__left_key()
                left_key_flg = False
            elif left_key:
                left_key_flg = True

            if not center_key and center_key_flg :
                self.__center_key()
                center_key_flg = False
            elif center_key:
                center_key_flg = True

            if not right_key and right_key_flg :
                self.__right_key()
                right_key_flg = False
            elif right_key:
                right_key_flg = True

            left   = self.keySW_main.GPIO_B_input(port=2)
            center = self.keySW_main.GPIO_B_input(port=1)
            right  = self.keySW_main.GPIO_B_input(port=0)

            if left and center and right:
                self.keySW_main.GPIO_B_output(port=5, on=1)
                self.keySW_main.GPIO_B_output(port=6, on=0)
                break
            else :
                self.keySW_main.GPIO_B_output(port=5, on=0)
                self.keySW_main.GPIO_B_output(port=6, on=1)

