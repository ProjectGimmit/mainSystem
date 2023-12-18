import time
from mcp23017 import MCP23017

timer_mcp = MCP23017(0x20)
timer_mcp.GPIO_A_init(0x00)

# 出力する数値の設定
def num_on(number : int):
  num_bin = list(map(int, format(number, 'b').zfill(4)))
  num_bin.reverse()

  # 表示する数値の信号設定
  for i in range(4) :
    timer_mcp.GPIO_A_output(i, num_bin[i])

# 7セグの点灯用
def on_7seg(digit : int) :
  """
  digit_num: 点灯する桁の位置 1〜4
  """
  digit_num = 4
  if 1 <= digit and digit <= 4:
    digit_num = 3 + digit

  # カソードコモン7セグ用
  # 0(GND)にすることで点灯させることができる
  timer_mcp.GPIO_A_output(digit_num, 0)
  timer_mcp.GPIO_A_output(digit_num, 1)

