import mcp23017

class Lightsout():
    def __init__(self) -> None:
        self.lightsout_out = mcp23017.MCP23017(0x24)
        self.lightsout_out.GPIO_A_init(0x00)
        self.lightsout_out.GPIO_B_init(0x00)

        self.lightsout_in = mcp23017.MCP23017(0x25)
        self.lightsout_in.GPIO_A_init(0xFF)
        self.lightsout_in.GPIO_B_init(0xFF)
    
    #-----------
    # 初期設定
    #-----------
    def __init_gimmick(self, lightsout: any):
        self.lights_list: list[bool] = lightsout["default"]
        self.lightsout_out.GPIO_A_output(port=0, on=1 if self.lights_list[0] else 0)
        self.lightsout_out.GPIO_A_output(port=1, on=1 if self.lights_list[1] else 0)
        self.lightsout_out.GPIO_A_output(port=2, on=1 if self.lights_list[2] else 0)
        self.lightsout_out.GPIO_A_output(port=3, on=1 if self.lights_list[3] else 0)
        self.lightsout_out.GPIO_A_output(port=4, on=1 if self.lights_list[4] else 0)
        self.lightsout_out.GPIO_A_output(port=5, on=1 if self.lights_list[5] else 0)
        self.lightsout_out.GPIO_A_output(port=6, on=1 if self.lights_list[6] else 0)
        self.lightsout_out.GPIO_A_output(port=7, on=1 if self.lights_list[7] else 0)
        self.lightsout_out.GPIO_B_output(port=0, on=1 if self.lights_list[8] else 0)

    #-----------
    # 上 左
    #-----------
    def __click_top_left(self):
        self.lights_list[6] = not self.lights_list[6]
        self.lights_list[7] = not self.lights_list[7]
        self.lights_list[3] = not self.lights_list[3]

    #-----------
    # 上 中
    #-----------
    def __click_top_mid(self):
        self.lights_list[6] = not self.lights_list[6]
        self.lights_list[7] = not self.lights_list[7]
        self.lights_list[8] = not self.lights_list[8]
        self.lights_list[4] = not self.lights_list[4]

    #-----------
    # 上 右
    #-----------
    def __click_top_right(self):
        self.lights_list[7] = not self.lights_list[7]
        self.lights_list[8] = not self.lights_list[8]
        self.lights_list[5] = not self.lights_list[5]

    #-----------
    # 中 左
    #-----------
    def __click_mid_left(self):
        self.lights_list[6] = not self.lights_list[6]
        self.lights_list[3] = not self.lights_list[3]
        self.lights_list[4] = not self.lights_list[4]
        self.lights_list[0] = not self.lights_list[0]

    #-----------
    # 中 中
    #-----------
    def __click_mid_mid(self):
        self.lights_list[7] = not self.lights_list[7]
        self.lights_list[3] = not self.lights_list[3]
        self.lights_list[4] = not self.lights_list[4]
        self.lights_list[5] = not self.lights_list[5]
        self.lights_list[1] = not self.lights_list[1]

    #-----------
    # 中 右
    #-----------
    def __click_mid_right(self):
        self.lights_list[8] = not self.lights_list[8]
        self.lights_list[4] = not self.lights_list[4]
        self.lights_list[5] = not self.lights_list[5]
        self.lights_list[2] = not self.lights_list[2]

    #-----------
    # 下 左
    #-----------
    def __click_btm_left(self):
        self.lights_list[3] = not self.lights_list[3]
        self.lights_list[0] = not self.lights_list[0]
        self.lights_list[1] = not self.lights_list[1]

    #-----------
    # 下 中
    #-----------
    def __click_btm_mid(self):
        self.lights_list[4] = not self.lights_list[4]
        self.lights_list[0] = not self.lights_list[0]
        self.lights_list[1] = not self.lights_list[1]
        self.lights_list[2] = not self.lights_list[2]

    #-----------
    # 下 右
    #-----------
    def __click_btm_right(self):
        self.lights_list[5] = not self.lights_list[5]
        self.lights_list[1] = not self.lights_list[1]
        self.lights_list[2] = not self.lights_list[2]

    #-------
    # 停止
    #-------
    def stop(self):
        self.lightsout_out.GPIO_A_output(port=0, on=0)
        self.lightsout_out.GPIO_A_output(port=1, on=0)
        self.lightsout_out.GPIO_A_output(port=2, on=0)
        self.lightsout_out.GPIO_A_output(port=3, on=0)
        self.lightsout_out.GPIO_A_output(port=4, on=0)
        self.lightsout_out.GPIO_A_output(port=5, on=0)
        self.lightsout_out.GPIO_A_output(port=6, on=0)
        self.lightsout_out.GPIO_A_output(port=7, on=0)
        self.lightsout_out.GPIO_B_output(port=0, on=0)
        self.lightsout_out.GPIO_B_output(port=1, on=0)
        self.lightsout_out.GPIO_B_output(port=2, on=0)

    
    def loop(self, lightsout: any):
        self.__init_gimmick(lightsout)
        self.lightsout_out.GPIO_B_output(port=1, on=0)
        self.lightsout_out.GPIO_B_output(port=2, on=1)

        while True:
            check_flg = True
            top_left  = self.lightsout_in.GPIO_A_input(port=6)
            top_mid   = self.lightsout_in.GPIO_A_input(port=7)
            top_right = self.lightsout_in.GPIO_B_input(port=0)
            mid_left  = self.lightsout_in.GPIO_A_input(port=3)
            mid_mid   = self.lightsout_in.GPIO_A_input(port=4)
            mid_right = self.lightsout_in.GPIO_A_input(port=5)
            btm_left  = self.lightsout_in.GPIO_A_input(port=0)
            btm_mid   = self.lightsout_in.GPIO_A_input(port=1)
            btm_right = self.lightsout_in.GPIO_A_input(port=2)

            if not top_left:
                self.__click_top_left()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=6): break

            elif not top_mid:
                self.__click_top_mid()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=7): break

            elif not top_right:
                self.__click_top_right()
                while True:
                    if self.lightsout_in.GPIO_B_input(port=0): break

            elif not mid_left:
                self.__click_mid_left()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=3): break

            elif not mid_mid:
                self.__click_mid_mid()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=4): break

            elif not mid_right:
                self.__click_mid_right()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=5): break

            elif not btm_left:
                self.__click_btm_left()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=0): break

            elif not btm_mid:
                self.__click_btm_mid()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=1): break

            elif not btm_right:
                self.__click_btm_right()
                while True:
                    if self.lightsout_in.GPIO_A_input(port=2): break

            for i in range(9):
                if self.lights_list[i] == True:
                    check_flg = False

            self.lightsout_out.GPIO_A_output(port=0, on=1 if self.lights_list[0] else 0)
            self.lightsout_out.GPIO_A_output(port=1, on=1 if self.lights_list[1] else 0)
            self.lightsout_out.GPIO_A_output(port=2, on=1 if self.lights_list[2] else 0)
            self.lightsout_out.GPIO_A_output(port=3, on=1 if self.lights_list[3] else 0)
            self.lightsout_out.GPIO_A_output(port=4, on=1 if self.lights_list[4] else 0)
            self.lightsout_out.GPIO_A_output(port=5, on=1 if self.lights_list[5] else 0)
            self.lightsout_out.GPIO_A_output(port=6, on=1 if self.lights_list[6] else 0)
            self.lightsout_out.GPIO_A_output(port=7, on=1 if self.lights_list[7] else 0)
            self.lightsout_out.GPIO_B_output(port=0, on=1 if self.lights_list[8] else 0)

            if check_flg:
                self.lightsout_out.GPIO_B_output(port=1, on=1)
                self.lightsout_out.GPIO_B_output(port=2, on=0)
                break
            else:
                self.lightsout_out.GPIO_B_output(port=1, on=0)
                self.lightsout_out.GPIO_B_output(port=2, on=1)
