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
from dronekit import connect, VehicleMode, LocationGlobalRelative

mavlink_connection_string = pymavlink.mavutil.mavlink_connection("udp:localhost:14550")

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    print('Starting SITL...')
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

#Derived partially from https://github.com/willgower/es410_autonomous_drone/blob/master/raspberry_pi/flight_controller.py
#TODO: Split this code off into utility functions
#Arguments: The target point of type dronekit.LocationGlobalRelative
def distance_to_point(point):
    try:
        return get_distance_metres(vehicle.location.global_frame, point)
    except:
        return "Could not determine distance to point."

    
def get_distance_metres(location_1, location_2):
    """
    Returns the ground distance in metres between two LocationGlobalRelative objects.
    Modified from dronekit example documentation
    The final term deals with the earths curvature

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = location_2.lat - location_1.lat
    dlong = location_2.lon - location_1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5




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
# The time_seconds parameter is optional.
def wait_for_arrival(location, wait_time_seconds=20):
    print("Going to (%f, %f). Timeout after %d seconds." % (location.lat, location.lon, wait_time_seconds))
    start_time = time.time()
    # This function returns a result in metres.
    distance = distance_to_point(location)
    while distance > 0.75:
        if(time.time() - start_time > wait_time_seconds):
            print("Time for travel exceeded specified wait time of %d seconds at distance %dm remaining, continuing with next command." % (wait_time_seconds, distance))
            break # Exit the loop
        print("Approaching point with distance %dm remaining." % (distance))
        time.sleep(1)
        distance = distance_to_point(location)

    if(distance < 0.75):
        print("Reached point within acceptable range.")
    return

# Function to check if the flight controller acknowledged the command.
# Unfortunately by the time this function is called, the message has already been sent.
# Function not currently used, may need Threading.
def wait_for_mission_ack(mavlink_connection_string):
    while True:
        # Wait for a message to be received
        msg = mavlink_connection_string.recv_match(blocking=False, timeout=5)
        if msg is not None:
            # If the message is a MISSION_ACK message, return the message
            if msg.get_type() == "MISSION_ACK":
                return msg
            # If the message is not a MISSION_ACK message, continue waiting
            else:
                continue


arm_and_takeoff(10)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

point1 = LocationGlobalRelative(52.37419420, -1.56527820, 10)
vehicle.simple_goto(point1)
wait_for_arrival(point1, 25)

point2 = LocationGlobalRelative(52.37480830, -1.56521920, 10)
vehicle.simple_goto(point2, groundspeed=10)
wait_for_arrival(point2, 25)

point3 = LocationGlobalRelative(52.37480010, -1.56431260, 10)
vehicle.simple_goto(point3)
wait_for_arrival(point3, 25)

point4 = LocationGlobalRelative(52.37416480, -1.56435280, 10)
vehicle.simple_goto(point4)
wait_for_arrival(point4, 25)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()


