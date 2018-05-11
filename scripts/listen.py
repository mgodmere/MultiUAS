# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

fcu_c = 20100
url = '127.0.0.1:' + str(fcu_c + int(sys.argv[1]))
print 'Listening on ' + url
vehicle = connect(url, wait_ready=True)

@vehicle.on_message('*')
def listener(self, name, message):
	print 'message: %s' % message

while(True):
	time.sleep(1)
