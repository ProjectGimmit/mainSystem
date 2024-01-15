import mcp23017

class Wires():
    def __init__(self) -> None:
        self.wires_main = mcp23017.MCP23017(0x20)
        self.wires_main.GPIO_A_init(0x00) # 出力
        self.wires_main.GPIO_B_init(0xFF) # 入力
    
    #-----------
    # 初期設定
    #-----------
    def __init_gimmick(self, wires: any):
        self.ANSWER = wires["answer"]

    #-------
    # 停止
    #-------
    def stop(self):
        self.wires_main.GPIO_A_output(port=1, on=0)
        self.wires_main.GPIO_A_output(port=0, on=0)

    #---------
    # メイン
    #---------
    def loop(self, wires: any):
        self.__init_gimmick(wires)
        self.wires_main.GPIO_A_output(port=1, on=0)
        self.wires_main.GPIO_A_output(port=0, on=1)

        while True:
            red_wire    = self.wires_main.GPIO_B_input(port=0)
            yellow_wire = self.wires_main.GPIO_B_input(port=1)
            green_wire  = self.wires_main.GPIO_B_input(port=2)
            blue_wire   = self.wires_main.GPIO_B_input(port=3)

            result = [not red_wire, not yellow_wire, not green_wire, not blue_wire]

            if result == self.ANSWER:
                self.wires_main.GPIO_A_output(port=1, on=1)
                self.wires_main.GPIO_A_output(port=0, on=0)
                break
            else:
                self.wires_main.GPIO_A_output(port=1, on=0)
                self.wires_main.GPIO_A_output(port=0, on=1)
