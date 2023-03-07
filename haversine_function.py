# Import necessary math functions
from math import sin, cos, atan2, sqrt, radians

# Define function to calculate North/South and East/West differences between two points
def get_distance_haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the North/South and East/West differences in meters between two points
    with the given latitude and longitude coordinates using the Haversine formula.
    """
    R = 6371e3  # Earth's radius in meters

    # Convert latitude and longitude values from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences in latitude and longitude between the two points
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the Haversine formula components
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance between the two points in meters
    distance = R * c

    # Calculate the North/South and East/West differences in meters
    dy = distance * dlat / c
    dx = distance * cos(0.5 * (lat1 + lat2)) * dlon / c

    # Return the East/West and North/South differences as a tuple
    return dx, dy

# Define the latitude and longitude values for the two points
lat1, lon1 = 40.754, -73.984
lat2, lon2 = 40.754, -73.984 + 24.1482e-6

# Call the get_distance function to calculate the North/South and East/West differences
dx, dy = get_distance_haversine(lat1, lon1, lat2, lon2)

# Print the North/South and East/West differences
print("dx = {:.6f} m, dy = {:.6f} m".format(dx, dy))
