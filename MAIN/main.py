import sys
from mcp23017 import MCP23017


from toggleSW import ToggleSW
from keySW import KeySW
from level import Level
from lightsout import Lightsout

from MAIN.modules.edit_json import read_config

#-----------
# toggleSW
#-----------
toggleSW = ToggleSW()

#-----------
# keySW
#-----------
keySW = KeySW()

#-----------
# level
#-----------
level = Level()

#-----------
# lightsout
#-----------
lightsout = Lightsout()


def main_process() :

	config = read_config()
	print(config)

	# toggleSW.stop()
	# keySW.stop()
	# level.stop()
	# lightsout.stop()

	# print("toggleSW")
	# toggleSW.loop()

	# print("keySW")
	# keySW.loop()

	# print("level")
	# level.loop()
	
	# print("lightsout")
	# lightsout.loop()

	# print("end")
	
	# toggleSW.stop()
	# keySW.stop()
	# level.stop()
	# lightsout.stop()





try:
	main_process()

except KeyboardInterrupt:
	sys.exit()
