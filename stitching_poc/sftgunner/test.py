import cv2
from time import sleep
import glob
# image_paths = glob.glob('dji/*.jpg')
image_paths = glob.glob('stitching_poc/UAV-Image-stitching/lores/*.png')
# image_paths=['1.png','2.png','3.png']
# initialized a list of images
imgs = []

print(image_paths)

limit = 2
#limit = len(image_paths)
 
for i in range(limit):
    # hir2 = cv2.pyrUp(hir1)
    imgs.append(cv2.pyrUp(cv2.pyrUp(cv2.imread(image_paths[i]))))
    imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.4,fy=0.4)
    # this is optional if your input images isn't too large
    # you don't need to scale down the image
    # in my case the input images are of dimensions 3000x1200
    # and due to this the resultant image won't fit the screen
    # scaling down the images
# showing the original pictures
cv2.imshow('1',imgs[0])
cv2.waitKey(0)
# cv2.imshow('2',imgs[1])
# cv2.waitKey(0)
# cv2.imshow('3',imgs[2])
# cv2.waitKey(0)
# cv2.imshow('4',imgs[3])
# cv2.imshow('5',imgs[4])

output = imgs[0]

for i in range(1,limit):
    images_to_stitch = [output,imgs[i]]
    print("Initialising stitcher") 
    stitchy=cv2.Stitcher.create()
    print("Attempting stitch for images "+str(i-1)+" and "+str(i))
    (dummy,output)=stitchy.stitch(imgs)
 
    if dummy != cv2.STITCHER_OK:
    # checking if the stitching procedure is successful
    # .stitch() function returns a true value if stitching is
    # done successfully
        raise Exception("stitching ain't successful")
    else:
        print("Succeeded stitch for images "+str(i-1)+" and "+str(i))
 
print("Completed all stitches successfully")
# final output
cv2.imshow('final result',output)
 
cv2.waitKey(0)

