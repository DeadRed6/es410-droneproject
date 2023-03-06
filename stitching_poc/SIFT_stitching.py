# Image Stitching with ORB and FLANN

import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob

# For debugging have numpy display in non-scientific notation (easier to see when homography approximately identity)
np.set_printoptions(suppress=True)

def stitching(img1, img2, H): # Define function for stitching the images
  rows1, cols1 = img1.shape[:2]
  rows2, cols2 = img2.shape[:2]

  points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2) #coordinates of a reference image
  
  temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2) #coordinates of second image

  points_2 = cv2.perspectiveTransform(temp_points, H) # Calculate the transformation matrix for Homography (planar transformation)

  points = np.concatenate((points_1,points_2), axis=0)

  [x_min, y_min] = np.int32(points.min(axis=0).ravel() - 0.5)
  [x_max, y_max] = np.int32(points.max(axis=0).ravel() + 0.5)
  
  translation_dist = [-x_min,-y_min] # Translation distance required for transform
  
  H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]]) # Defining the Homography translation

  output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min)) # Warping the image based on Homography matrix
  output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

  return output_img

path = sorted(glob.glob("./Thermal-Images-Test1/*.jpg")) # Read all images in current folder which is a JPEG
img_list = []
for img in path:
    n = cv2.imread((img)) 
    img_list.append(n)

nfeatures = 20000 # Assign number of features to find in image

orb = cv2.SIFT_create(nfeatures) # Defining ORB variable to use the ORB algorithm to extract features of image
while True:
  if len(img_list) == 0:
    break
  img1=img_list.pop(0)
  img2=img_list.pop(0)
  kp1, des1 = orb.detectAndCompute(img1, None) # Finding keypoints and descriptors of the image
  kp2, des2 = orb.detectAndCompute(img2, None)
  visualiser = cv2.drawKeypoints(img1, kp1, None, color=(0,255,0), flags=0) # Define variabl to visualise the features the algorithm has detected
  plt.imshow(cv2.cvtColor(visualiser, cv2.COLOR_BGR2RGB)), plt.show() # Visualise the variable

  FLANN_INDEX_KDTREE = 0
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5) # Setting parameters for input for FLANN matcher
  search_params = dict(checks = 50) 
  flann = cv2.FlannBasedMatcher(index_params, search_params) # Defining varaible for FLANN algorithm
  matches = flann.knnMatch(des1,des2,k=2) # Use k nearest neighbours to find matches on image
  
  all_matches = []
  for m, n in matches: # Defining a threshold for matches so only good matches are used
    all_matches.append(m)
  good = []
  for m, n in matches:
    if m.distance < 0.6 * n.distance:
      good.append(m)

  MIN_MATCHES = 1 # Setting a mim=nimum matches condition for FLANN algorithm 

  if len(good) > MIN_MATCHES:
    
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2) # Using keypoints to calculate source and destination points for Homography
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    err_thresh = 2 # Setting an error threshold for Homography
    M, _= cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,err_thresh) # Definifng a Homography 
    print(M) 

    result = stitching(img2, img1, M)  # Stitch the images based on Homography matrix
    print(result)

    img_list.insert(0,result)
    print("Reinserting result composite (GOOD) with "+str(len(good))+" matches") # Using stitched image as input for loop
    print("Resolution of composite image is "+str(result.shape[1])+" x "+str(result.shape[0]))
    
    if len(img_list)==1:
      break
    
  else:
    print("Failed to match with only "+str(len(good))+" matches") # When matches criteria isn't met, reinsert stitched image so far
    print("Reinserting current composite image (BAD)")
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB ))
    plt.show()
    img_list.insert(0,img1)
    if len(img_list)==1:
      break
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB )  
plt.imshow(result) # Showuing result of stitched image
plt.show()

