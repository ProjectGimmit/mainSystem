import smbus
import time
from mcp23017 import MCP23017

CHANNEL   = 1       # i2c割り当てチャンネル 1 or 0
I2CADDR    = 0x20   # MCP23017のアドレス。この場合はA0~A3までGND接続した場合のアドレス。
REG_IODIRA = 0x00    # 入出力設定レジスタ
REG_GPIOA  = 0x12   # 入出力レジスタ

bus = smbus.SMBus(CHANNEL)  #smbusを定義

mcp23017_1 = MCP23017(I2CADDR)
mcp23017_1.GPIO_A_init(REG_GPIOA, REG_IODIRA, 0x80)

# ピンの入出力設定
# bus.write_byte_data(I2CADDR, REG_IODIRA, 0x80)   #データシートより、0:出力 0b10000000
def loop():
    while True:


        # GPA0をONする
        # bus.write_byte_data(32, REG_GPIOA, 1)
        # mcp23017_1.GPIO_A_output(0, 1)


        # time.sleep(1)
        # ポート8の入力状態を取得する
        # result = getInput(7, REG_GPIOA)
        mcp23017_1.GPIO_A_output(0, 0)
        result = mcp23017_1.GPIO_A_input(7)

        if not result:
            mcp23017_1.GPIO_A_output(0, 1)
            while True:
                res = mcp23017_1.GPIO_A_input(7)
                if res :
                    break
                # print("AND演算の結果:", result)
                # decimal_number = bus.read_byte_data(32,REG_GPIOA)
                # print(decimal_number)
                # time.sleep(0.3)
        
        decimal_number = bus.read_byte_data(32,REG_GPIOA)

        # time.sleep(1)


def getInput(port, reg_gpio):
    """
    指定したポートの入力状態を取得する
    ----------------------------------
    port     : ポートの位置
    reg_gpio : 
    """
    # 2進数に変換
    binary_value = int(bin(1 << port), 2)
    hoge = bin(binary_value ^ 0b11111111)
    # print("bin   : ", bin(1 << (port - 1)))
    # print("bin_r : ", hoge)
    # print("port : ", binary_value)
    decimal_number = bus.read_byte_data(I2CADDR,reg_gpio)
    return bool(decimal_number & binary_value)

# Ctrl+Cキーで入る。
def destroy():
    bus.write_byte_data(I2CADDR, REG_GPIOA, 0x00)
    print('end')


# main
if __name__ == '__main__':
    print ('Program is starting...' )
    try:
        loop() 
    # ターミナル上でCtrl+Cでloop()を中断
    except KeyboardInterrupt: 
        destroy()