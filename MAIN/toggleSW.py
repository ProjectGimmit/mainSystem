import random
import time
from mcp23017 import MCP23017



class ToggleSW:
    def __init__(self) -> None:
        self.toggleSW_main = MCP23017(0x21)
        self.toggleSW_main.GPIO_A_init(0xFF)  # 入力
        self.toggleSW_main.GPIO_B_init(0x00)  # 出力
    
    #-----------
    # 初期設定
    #-----------
    def __init_gimmick(self, toggleSW_config: any):
        # self.ANSWER = random.randint(0, 31)
        answer_num = 0
        for i, v in enumerate(toggleSW_config["answer"]):
            if v:
                answer_num += 2 ** i 
        self.ANSWER = answer_num
        print(self.ANSWER)
    
    # ---------------------
    # 出力する数値の設定
    # ---------------------
    def __set_num(self, number: int):
        num_bin = list(map(int, format(number, "b").zfill(4)))
        num_bin.reverse()
        # 表示する数値の信号設定
        for i in range(4):
            self.toggleSW_main.GPIO_B_output(i, num_bin[i])

    # ----------------
    # 7セグの点灯用
    # ----------------
    def __on_7seg(self, digit: int):
        """
        digit_num: 点灯する桁の位置 1〜2
        """
        digit_num = 4
        if 1 <= digit and digit <= 2:
            digit_num = 3 + digit

        # カソードコモン7セグ用
        # 0(GND)にすることで点灯させることができる
        self.toggleSW_main.GPIO_B_output(digit_num, 0)
        time.sleep(0.005)
        self.toggleSW_main.GPIO_B_output(digit_num, 1)

    # ------------------------
    # 7セグメントの数値表示
    # ------------------------
    def __num_7seg(self, num: int):
        nums = list(str(num).zfill(2))
        for i, v in enumerate(nums):
            self.__set_num(int(v))
            self.__on_7seg(2 - i)
    #-------------
    # スタンバイ
    #-------------
    def standby(self):
        self.toggleSW_main.GPIO_B_output(port=6, on=0)
        self.toggleSW_main.GPIO_B_output(port=7, on=1)

    #-------
    # 停止
    #-------
    def stop(self):
        self.toggleSW_main.GPIO_B_output(port=4, on=1)
        self.toggleSW_main.GPIO_B_output(port=5, on=1)
        self.toggleSW_main.GPIO_B_output(port=6, on=0)
        self.toggleSW_main.GPIO_B_output(port=7, on=0)

    #---------
    # メイン
    #---------
    def loop(self, toggleSW_config: any):
        self.__init_gimmick(toggleSW_config)
        self.toggleSW_main.GPIO_B_output(port=6, on=0)
        self.toggleSW_main.GPIO_B_output(port=7, on=1)

        while True:
            sw_sum = 0
            self.__num_7seg(self.ANSWER)
            sw1 = self.toggleSW_main.GPIO_A_input(port=4)
            if not sw1:
                sw_sum += 1
            sw2 = self.toggleSW_main.GPIO_A_input(port=3)
            if not sw2:
                sw_sum += 2
            sw3 = self.toggleSW_main.GPIO_A_input(port=2)
            if not sw3:
                sw_sum += 4
            sw4 = self.toggleSW_main.GPIO_A_input(port=1)
            if not sw4:
                sw_sum += 8
            sw5 = self.toggleSW_main.GPIO_A_input(port=0)
            if not sw5:
                sw_sum += 16

            if self.ANSWER == sw_sum:
                self.toggleSW_main.GPIO_B_output(port=6, on=1)
                self.toggleSW_main.GPIO_B_output(port=7, on=0)
                break
            else:
                self.toggleSW_main.GPIO_B_output(port=6, on=0)
                self.toggleSW_main.GPIO_B_output(port=7, on=1)
        self.toggleSW_main.GPIO_B_output(port=4, on=1)
        self.toggleSW_main.GPIO_B_output(port=5, on=1)

