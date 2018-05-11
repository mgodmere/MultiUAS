# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

fcu_c = 20100

def ArmTakeoff(vehicles, alt):
	for vehicle in vehicles:
		print "Basic pre-arm checks"
		# Don't try to arm until autopilot is ready
		while not vehicle.is_armable:
			print " Waiting for vehicle to initialise..."
			time.sleep(1)

		print "Arming motors"
		# Copter should arm in GUIDED mode
		vehicle.mode    = VehicleMode("GUIDED")
		vehicle.armed   = True

		# Confirm vehicle armed before attempting to take off
		while not vehicle.armed:
			print " Waiting for arming..."
			time.sleep(1)

		print "Taking off!"
		vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

		# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
		#  after Vehicle.simple_takeoff will execute immediately).
		while True:
			print " Altitude: ", vehicle.location.global_relative_frame.alt
			#Break and return from function just below target altitude.
			if vehicle.location.global_relative_frame.alt >= alt * 0.95:
				print "Reached target altitude"
				break
			time.sleep(1)

def main():
	vehicles = []

	# connect
	for i in range(0,int(sys.argv[1])):
		url = '127.0.0.1:' + str(fcu_c + i + 1)
		print 'Connecting to ' + url
		vehicles.append(connect(url, wait_ready=True))

	ArmTakeoff(vehicles, 5)

if __name__ == "__main__":
	main()
