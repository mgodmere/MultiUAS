from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

off = 20000
MAV_MODE_AUTO = 4
spacing = 2

def SetMode(vehicles, mavMode):
	for vehicle in vehicles:
	    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
	                                               mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
	                                               mavMode,
	                                               0, 0, 0, 0, 0, 0)

def get_location_offset_meters(original_location, dNorth, dEast, alt):
	"""
	Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
	specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
	The function is useful when you want to move the vehicle around specifying locations relative to
	the current vehicle position.
	The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
	For more information see:
	http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
	"""
	earth_radius=6378137.0 #Radius of "spherical" earth
	#Coordinate offsets in radians
	dLat = dNorth/earth_radius
	dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

	#New position in decimal degrees
	newlat = original_location.lat + (dLat * 180/math.pi)
	newlon = original_location.lon + (dLon * 180/math.pi)
	return LocationGlobal(newlat, newlon,original_location.alt+alt)

# connect
vehicles = []
for i in range(0,int(sys.argv[1])):
	url = '127.0.0.1:' + str(off + i)
	vehicles.append(connect(url, wait_ready=False))

# Change to AUTO mode
SetMode(vehicles, MAV_MODE_AUTO)

# load mission
index = 1
for vehicle in vehicles:
	cmds = vehicle.commands
	cmds.clear()
	vehicle.flush()

	# takeoff
	wp = get_location_offset_meters(vehicle.location.global_relative_frame, 0, 0, 30);
	cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
	cmds.add(cmd)

	# Upload mission
	cmds.upload()
	vehicle.flush()
	index += 1

# arm vehicles
for vehicle in vehicles:
	vehicle.armed = True
