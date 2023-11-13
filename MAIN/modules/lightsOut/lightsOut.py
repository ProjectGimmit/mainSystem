import smbus
import time
from MAIN.modules.mcp23017 import MCP23017


"""
状態LED
  緑 赤
  B1 B2

ボタン配置
  A6 A7 B0
  A3 A4 A5
  A0 A1 A2
"""

OUTPUTI2CADDR = 0x24
INPUTI2CADDR = 0x25

mcp_input = MCP23017(INPUTI2CADDR)  # 入力レジスタ
mcp_input.GPIO_A_init(0x00)
mcp_input.GPIO_B_init(0x00)
mcp_output = MCP23017(OUTPUTI2CADDR)  # 出力レジスタ
mcp_output.GPIO_A_init(0xFF)
mcp_output.GPIO_B_init(0xFF)

btnToggle = False

def loop():
    while True:

        # top
        topLeft  = mcp_input.GPIO_A_input(6)
        topMid   = mcp_input.GPIO_A_input(7)
        topRight = mcp_input.GPIO_B_input(0)
        # mid
        midLeft  = mcp_input.GPIO_A_input(3)
        midMid   = mcp_input.GPIO_A_input(4)
        midRight = mcp_input.GPIO_A_input(5)
        # btm
        btmLeft  = mcp_input.GPIO_A_input(0)
        btmMid   = mcp_input.GPIO_A_input(1)
        btmRight = mcp_input.GPIO_A_input(2)

        # TOP_LEFT
        if not mcp_input.GPIO_A_input(6) :
            btnToggle = True

            while btnToggle :
                if mcp_input.GPIO_A_input(6) :
                    btnToggle = False
        # TOP_MID
        # TOP_RIGHT

        # MID_LEFT
        # MID_MID
        # MID_RIGHT

        # BTM_LEFT
        # BTM_MID
        # BTM_RIGHT
        mcp23017_1.GPIO_A_output(0, 0)
        # result = mcp23017_1.GPIO_A_input(7)

        if not mcp23017_1.GPIO_A_input(7):
            mcp23017_1.GPIO_A_output(0, 1)
            while True:
                if mcp23017_1.GPIO_A_input(7):
                    break


# Ctrl+Cキーで入る。
def destroy():
    print("end")


# main
if __name__ == "__main__":
    print("Program is starting...")
    try:
        loop()
    # ターミナル上でCtrl+Cでloop()を中断
    except KeyboardInterrupt:
        destroy()
