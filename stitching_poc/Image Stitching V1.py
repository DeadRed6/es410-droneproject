from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True, help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True, help="path to output image")
args = vars(ap.parse_args())


print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []
for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	images.append(image)

print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)
if status == 0:
	cv2.imwrite(args["output"], stitched)
	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)

else:
	print("[INFO] image stitching failed ({})".format(status))
