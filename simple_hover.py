#!/usr/bin/env python
# -*- coding: utf-8 -*-


# To be run on a Linux system.
"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time, math
import pymavlink
import helpers
#from helpers import WaypointParser, broadcast_gps
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import dronekit_sitl

mavlink_connection_string = pymavlink.mavutil.mavlink_connection("udp:localhost:14550")

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string, e.g. udp:localhost:14550 or /dev/tty/ACM0. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = dronekit_sitl.SITL()


# Start SITL if no connection string specified
if not connection_string:
    print('Starting SITL...')
    sitl.download('copter', '3.3', verbose=True)
    sitl_args = ['-I0', '--model', 'quad', '--home=52.37400919,-1.5657824,0,0']
    sitl.launch(sitl_args, await_ready=True, restart=True)
    #sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")

    # Must wait for this to go through
    while not vehicle.mode.name=='GUIDED':  #Wait until mode has changed
        print(" Waiting for mode change ...")
        time.sleep(1)

    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Monitor the position of the drone, and move on to the next command once within a certain distance of the target

arm_and_takeoff(1)
time.sleep(10)


vehicle.mode = VehicleMode("LAND")

while not vehicle.mode.name=='LAND':  #Wait until mode has changed
    print(" Waiting for LAND mode change ...")
    time.sleep(1)


# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()


