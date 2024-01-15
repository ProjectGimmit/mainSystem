import time
import spidev
from mcp23017 import MCP23017
import copy
from collections import deque
from collections import Counter


class Level:
    #-----------------
    # コンストラクタ
    #-----------------
    def __init__(self) -> None:
        self.level_main = MCP23017(0x23)
        self.level_main.GPIO_A_init(0x00)  # 出力
        self.level_main.GPIO_B_init(0x00)  # 出力
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 3600000
        self.MAX = 958
        self.breakpoint: list[int] = []
        for i in range(1,11) :
            self.breakpoint.append(int((self.MAX/11) * i))
        self.level_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    #-----------
    # 初期設定
    #-----------
    def __init_gimmick(self, level_config: any):
        self.ANSWER = level_config["answer"]

    #-------
    # SPI読み取り
    #-------
    def __readAdc(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 200])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    #-------------
    # アナログ値からレベルへ変換
    #-------------
    def __convert_level(self, num) -> int:
        if self.breakpoint[0] > num: return 10
        elif self.breakpoint[0] <= num and num <= self.breakpoint[1] :return 9
        elif self.breakpoint[1] <= num and num <= self.breakpoint[2] :return 8
        elif self.breakpoint[2] <= num and num <= self.breakpoint[3] :return 7
        elif self.breakpoint[3] <= num and num <= self.breakpoint[4] :return 6
        elif self.breakpoint[4] <= num and num <= self.breakpoint[5] :return 5
        elif self.breakpoint[5] <= num and num <= self.breakpoint[6] :return 4
        elif self.breakpoint[6] <= num and num <= self.breakpoint[7] :return 3
        elif self.breakpoint[7] <= num and num <= self.breakpoint[8] :return 2
        elif self.breakpoint[8] <= num and num <= self.breakpoint[9] :return 1
        elif self.breakpoint[9] < num :return 0

    #-----------------------
    # ノイズ対策用メソッド
    #-----------------------
    def __return_light_num(self, analog: int) -> int :
        level_num = self.__convert_level(analog)
        if len(self.level_list) < 10:
            self.level_list.append(self.level_list)
            return 0
        else :
            temp_list = copy.deepcopy(self.level_list)
            temp_list = deque(temp_list)
            temp_list.popleft()
            temp_list.append(level_num)
            self.level_list = list(temp_list)
            self.level_list = list(self.level_list)
            
            counter = Counter(list(temp_list))
            # 一番多い要素を取得
            most_common_element = counter.most_common(1)[0][0]
            # print("集計：", most_common_element)
            return most_common_element


    #-------------
    # スタンバイ
    #-------------
    def standby(self):
        self.level_main.GPIO_B_output(port=2, on=0)
        self.level_main.GPIO_B_output(port=3, on=1)

    #-------
    # 停止
    #-------
    def stop(self):
        self.level_main.GPIO_A_output(port=0, on=0)
        self.level_main.GPIO_A_output(port=1, on=0)
        self.level_main.GPIO_A_output(port=2, on=0)
        self.level_main.GPIO_A_output(port=3, on=0)
        self.level_main.GPIO_A_output(port=4, on=0)
        self.level_main.GPIO_A_output(port=5, on=0)
        self.level_main.GPIO_A_output(port=6, on=0)
        self.level_main.GPIO_A_output(port=7, on=0)
        self.level_main.GPIO_B_output(port=0, on=0)
        self.level_main.GPIO_B_output(port=1, on=0)
        self.level_main.GPIO_B_output(port=2, on=0)
        self.level_main.GPIO_B_output(port=3, on=0)

    #---------
    # メイン
    #---------
    def loop(self, level_config: any):
        self.__init_gimmick(level_config)
        current_level = 0
        timer: float = 0
        flg = True
        print(self.ANSWER)
        self.level_main.GPIO_B_output(port=2, on=0)
        self.level_main.GPIO_B_output(port=3, on=1)

        while True:
            data = int(self.__readAdc(channel=0))
            current_level = self.__return_light_num(data)
            self.level_main.light_up_LED_Array(current_level)
            if current_level == self.ANSWER:
                if flg :
                    timer = time.perf_counter()
                    flg = False
            else :
                timer = time.perf_counter()
                flg = True

            if (time.perf_counter() - timer) > 3 :
                self.level_main.GPIO_B_output(port=2, on=1)
                self.level_main.GPIO_B_output(port=3, on=0)
                break
            else :
                self.level_main.GPIO_B_output(port=2, on=0)
                self.level_main.GPIO_B_output(port=3, on=1)

