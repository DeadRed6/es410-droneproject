import os
import pandas as pd
from dronekit import LocationGlobalRelative
from datetime import datetime

class WaypointParser:
    def __init__(self, filepath='./rugbypitch2.waypoints'):
        self.filepath = filepath
        self.waypoints = [] # Will be of type pandas.DataFrame
        self.next = 1 # Stores the next waypoint, starting at 1 since 0 is the home location
        self.total = 0 # Number of waypoints, including home and RTL.

        # Check if file exists
        if not os.path.exists(self.filepath):
            print("Error: File does not exist.")
            return
        
        # Read file
        with open(self.filepath, 'r') as f:
            # Exit gracefully if file is empty
            if os.stat(self.filepath).st_size == 0:
                print("Error: File is empty.")
                return
            
            # Format the file as a table
            self.waypoints = pd.read_table(self.filepath, sep='\t', skiprows=[0], header=None)
            
            # We only want the long, lat, and alt columns.
            self.waypoints = self.waypoints.drop(self.waypoints.columns[[0, 1, 2, 3, 4, 5, 6, 7, -1]], axis=1)

            # Rename the columns.
            self.waypoints.columns = ['Lat', 'Lon', 'Alt']

            # Count the number of waypoints as the number of rows in the table.
            self.total = self.waypoints.shape[0]

    # The .waypoints format reserves the first row for the home location
    def get_home_location(self):
        return LocationGlobalRelative(self.waypoints.iat[0, 0], self.waypoints.iat[0, 1], self.waypoints.iat[0, 2])

    # Returns the next waypoint in the file, or None if there are no more
    # The last waypoint will be 0,0,0 which indicates RTL (but this is for the caller to deal with).
    def get_next_waypoint(self):
        if(self.next + 1 > self.total):
            return None
        else:
            # DataFrame.iat : Access a single value for a row/column pair by integer position
            location = LocationGlobalRelative(self.waypoints.iat[self.next, 0], self.waypoints.iat[self.next, 1], self.waypoints.iat[self.next, 2])
            self.next += 1
            return location

#Print zeroes if the vehicle has no GPS lock, else print the coordinates
#Altitude is relative to the home location
def broadcast_gps(vehicle):
    location = vehicle.location.global_frame
    if(location.lat is None):
        print("[%s] lat=0.0 lon=0.0 alt=0.0" % (datetime.now()))
    else:
        print("[%s] lat=%s lon=%s alt=%s" % (datetime.now(), location.lat, location.lon, location.alt))

# Get all vehicle attributes (state)
def print_diagnostics(vehicle):
    print("\nGet all vehicle attribute values:")
    print(" Autopilot Firmware version: %s" % vehicle.version)
    print("   Major version number: %s" % vehicle.version.major)
    print("   Minor version number: %s" % vehicle.version.minor)
    print("   Patch version number: %s" % vehicle.version.patch)
    print("   Release type: %s" % vehicle.version.release_type())
    print("   Release version: %s" % vehicle.version.release_version())
    print("   Stable release?: %s" % vehicle.version.is_stable())
    print(" Autopilot capabilities")
    print("   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
    print("   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
    print("   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
    print("   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
    print("   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
    print("   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
    print("   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
    print("   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
    print("   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
    print("   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
    print("   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
    print("   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
    print("   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
    print("   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
    print(" Global Location: %s" % vehicle.location.global_frame)
    print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print(" Local Location: %s" % vehicle.location.local_frame)
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    print(" Gimbal status: %s" % vehicle.gimbal)
    print(" Battery: %s" % vehicle.battery)
    print(" EKF OK?: %s" % vehicle.ekf_ok)
    print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
    print(" Rangefinder: %s" % vehicle.rangefinder)
    print(" Rangefinder distance: %s" % vehicle.rangefinder.distance)
    print(" Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    print(" Heading: %s" % vehicle.heading)
    print(" Is Armable?: %s" % vehicle.is_armable)
    print(" System status: %s" % vehicle.system_status.state)
    print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
    print(" Airspeed: %s" % vehicle.airspeed)    # settable
    print(" Mode: %s" % vehicle.mode.name)    # settable
    print(" Armed: %s" % vehicle.armed)    # settable

def print_gps_diagnostics(vehicle):
    print("0/1=nofix. 2=2D-fix, 3=3D-fix 4=GNSS+dead reckoning")
    print("GPS (WGS84) Status: %s" % vehicle.gps_0)


# Uncomment this code if you want to test the class, simply run `python3 WaypointParser.py`
# def main():
#     # Create an instance of the WaypointParser class with the default filepath
#     parser = WaypointParser()
#     print(parser.total)
#     print(parser.waypoints.to_string())
#     print(parser.get_home_location())
    
#     for i in range(10):
#         print(parser.get_next_waypoint())

# if __name__ == '__main__':
#     main()