# UAV image stitching v2
# This version reads from a video file


#Import library
#import libraries
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# For debugging have numpy display in non-scientific notation (easier to see when homography approximately identity)
np.set_printoptions(suppress=True)

def crop(image):
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

def warpImages(img1, img2, H):
  rows1, cols1 = img1.shape[:2]
  rows2, cols2 = img2.shape[:2]

  list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2) #coordinates of a reference image
  temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2) #coordinates of second image

  # When we have established a homography we need to warp perspective
  # Change field of view
  list_of_points_2 = cv2.perspectiveTransform(temp_points, H)#calculate the transformation matrix

  list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

  [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
  [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
  
  translation_dist = [-x_min,-y_min]
  
  H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

  output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
  output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1
  
  # Crop output image
  output_img_cropped = crop(output_img)

  return output_img_cropped
#folder containing images from drones, sorted by name 
# import glob
# path = sorted(glob.glob("lores/*.png"))
# img_list = []
# for img in path:
#     n = cv2.pyrUp(cv2.pyrUp(cv2.imread(img)))
#     # n = cv2.imread(img)
#     img_list.append(n)
# """Functions for stitching"""


# Load video for processing
vidcap = cv2.VideoCapture('15m_altitude_downsampled_cropped.mp4')
# vidcap = cv2.VideoCapture('15m_altitude_full-res.MP4')
# Initialise image array
img_list = []

success,image = vidcap.read()
count = 0
while success:
  success,image = vidcap.read()
  # print('Read a new frame: ', success)
  # img_list.append(cv2.pyrUp(cv2.pyrUp(image)))
  img_list.append(image)

#Use ORB detector to extract keypoints
orb = cv2.ORB_create(nfeatures=20000)
while True:
  # Keep track of iterations so we can show image at regular intervals
  count = count + 1
  if len(img_list) == 0:
    break
  img1=img_list.pop(0)
  img2=img_list.pop(0)
# Find the key points and descriptors with ORB
  keypoints1, descriptors1 = orb.detectAndCompute(img1, None)#descriptors are arrays of numbers that define the keypoints
  keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
  
  # Visualise keypoints
  # draw only keypoints location,not size and orientation
  # visualiser = cv2.drawKeypoints(img1, keypoints1, None, color=(0,255,0), flags=0)
  # plt.imshow(cv2.cvtColor(visualiser, cv2.COLOR_BGR2RGB)), plt.show()


# Create a BFMatcher object to match descriptors
# It will find all of the matching keypoints on two images
  bf = cv2.BFMatcher_create(cv2.NORM_HAMMING2)#NORM_HAMMING specifies the distance as a measurement of similarity between two descriptors

# Find matching points
  matches = bf.knnMatch(descriptors1, descriptors2,k=2)

  all_matches = []
  for m, n in matches:
    all_matches.append(m)
# Finding the best matches
  good = []
  # threshold = 0.6
  threshold = 0.6
  for m, n in matches:
    if m.distance < threshold * n.distance:#Threshold
        good.append(m)

# Set minimum match condition
  MIN_MATCH_COUNT = 10 #10

  if len(good) > MIN_MATCH_COUNT:
    
    # Convert keypoints to an argument for findHomography
    src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    # Establish a homography
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0) # Proposing change from RANSAC to USAC_MAGSAC
    
    # M2 = cv2.estimateAffinePartial2D(src_pts, dst_pts)
    
    # num, Rs, Ts, Ns  = cv2.decomposeHomographyMat(M, np.eye(3))
    
    # print("Rotation:")
    # print(Rs)
    # print("Translation:")
    # print(Ts)
    # print("Normals:")
    # print(Ns)
    
    # print(M)
    
    # Ideally at this point the homography (i.e planar transform) should be pretty much identical to the identity matrix
    
    # Let's hack this so it is the identity matrix. 
    
    #M = np.eye(3)
    
    # try:
    result = warpImages(img2, img1, M)
    # except:
    #   print("Failure")
    #   break
    
    img_list.insert(0,result)
    print("Reinserting result composite (GOOD) with "+str(len(good))+" matches")
    if count % 100 == 0:
      print("On frame "+str(count))
      plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB )  )
      plt.show()
    print("Resolution of composite image is "+str(result.shape[1])+" x "+str(result.shape[0]))
    
    if len(img_list)==1:
      break
    
  else:
    print("Failed to match with only "+str(len(good))+" matches after "+str(count)+" frames")
    break
    # Reinsert the stitched image
    print("Reinserting current composite image (BAD)")
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB )  )
    plt.show()
    img_list.insert(0,img1)
    if len(img_list)==1:
      break
    

result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB )  
plt.imshow(result)
plt.show()
