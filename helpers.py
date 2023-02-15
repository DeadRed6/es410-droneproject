import os
import pandas as pd
from dronekit import LocationGlobalRelative
from datetime import datetime

class WaypointParser:
    def __init__(self, filepath='./coordinates.waypoints'):
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

#Print zeroes if the vehicle has no GPS lock, else print the absolute altitude
def broadcast_gps(vehicle):
    location = vehicle.location.global_frame
    if(location.lat is None):
        print("[%s] lat=0.0 lon=0.0 alt=0.0" % (datetime.now()))
    else:
        print("[%s] lat=%s lon=%s alt=%s" % (datetime.now(), location.lat, location.lon, location.alt))

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