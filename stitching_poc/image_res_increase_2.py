import cv2
import numpy as np
# import PIL
img = cv2.imread("stitching_poc/UAV-Image-stitching/lores/output_0002.png")

hir1 = cv2.pyrUp(img)
hir2 = cv2.pyrUp(hir1)
hir3 = cv2.pyrUp(hir2)

cv2.imshow("Original image", img)
cv2.imshow("First scaled up image", hir1)
cv2.imshow("Second scaled ip image", hir2)
cv2.imshow("Third scaled up image", hir3)

cv2.waitKey(0)
cv2.destroyAllWindows