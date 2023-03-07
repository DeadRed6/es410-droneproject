# Import necessary libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from haversine_function import get_distance_haversine
from math import tan, ceil

# Define camera parameters
CAMERA_ANGLE = 57  # Angle of view of the camera in degrees
ALTITUDE = 3  # Altitude of the camera in meters

# Define function to calculate frame size based on camera angle and altitude
def get_frame_size(camera_angle, altitude):
    """
    Calculates the size of the camera frame in meters based on camera angle and altitude.
    """
    frame_width = 2 * altitude * tan((camera_angle/2))*640
    frame_height = frame_width*3/4  # 3:4 frame aspect ratio
    return frame_width, frame_height

# Calculate frame size based on camera angle and altitude
FRAME_SIZE = get_frame_size(CAMERA_ANGLE, ALTITUDE)

# Read in images and their corresponding GPS coordinates
images = [cv2.imread('thermal1.jpg'), cv2.imread('thermal2.jpg')]
gps_coords = [(40.754, -73.984), (40.754, -73.984 + 24.1482e-6)]

# Calculate overlap between adjacent images based on their distance and frame size
overlaps = []
for i in range(len(images)-1):
    lat1, lon1 = gps_coords[i]
    lat2, lon2 = gps_coords[i+1]
    # Calculate distance between GPS coordinates using haversine formula
    dy, dx = get_distance_haversine(lat1, lon1, lat2, lon2)  # convert to meters
    overlap_x = int(FRAME_SIZE[0]-(FRAME_SIZE[0] - dx))*100  # calculate overlap in x-direction, convert to cm
    overlap_y = int(FRAME_SIZE[1]-(FRAME_SIZE[1] - dy))*100  # calculate overlap in y-direction, convert to cm
    overlaps.append((overlap_x, overlap_y))  # append overlaps to a list

# Create empty canvas for stitching images
max_x, max_y = np.max(np.cumsum(np.asarray(overlaps), axis=0), axis=0)
canvas = np.zeros((max_x + images[0].shape[0], max_y + images[0].shape[1], 3), np.uint8)

# Loop through each image and place it onto the canvas
x_offset, y_offset = 0, 0
for i, img in enumerate(images):
    if i == 0:  # first image does not need to be offset
        canvas[x_offset:x_offset+img.shape[0], y_offset:y_offset+img.shape[1]] = img
    else:
        overlap_x, overlap_y = overlaps[i-1]  # get overlap values for previous image
        x_offset += overlap_x  # update x offset by overlap value
        y_offset += overlap_y  # update y offset by overlap value
        canvas[x_offset:x_offset+img.shape[0], y_offset:y_offset+img.shape[1]] = img  # place image on canvas
# Display the stitched image
plt.imshow(canvas)
plt.show()

