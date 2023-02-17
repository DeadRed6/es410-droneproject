# Image Mosaic code for bisible light canera
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle

def ftr_keypoints(img, kp):
    img_kp = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)

    cv2.imshow('Keypoints', img_kp)
    cv2.waitkey(0)

def ftr_matches (img1, kp1, img2, kp2, matches):

    img3 = cv2.drawmatches(img1, kp1, img2, kp2, matches, None, flags=2)
    cv2.imshow('Matches', img3)

def reprojection_error(src_pts, dst_pts, H):
    error = 0
    for i in range(len(src_pts)):
        src_pt = src_pts[i]
        dst_pt = dst_pts[i]
        src_pt = np.append(src_pt, 1)
        transformed_pt = H @ src_pt
        transformed_pt = transformed_pt/transformed_pt[2]
        transformed_pt = transformed_pt[0:2]
        error += np.linalg.norm(transformed_pt - dst_pt)
    reproj_error = error/len(src_pts)

    return reproj_error

def stitching(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    points_1 = np.float32([[0,0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1,1,2)
    temporary_points =  np.float32([[0,0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1,1,2)
    points_2 = cv2.perspectiveTransform(temporary_points, H)
    points_concat = np.concatenate((points_1, points_2), axis=0)

    [x_min, y_min] = np.int32(points_concat.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(points_concat.max(axis=0).ravel() + 0.5)
    translation_dist = [-x_min, -y_min]
    Homogrophy_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0,0,1]])

    output_image = cv2.warpPerspective(img2, Homogrophy_translation.dot(H), (x_max - x_min, y_max - y_min))
    frame_size = output_image.shape
    new_image = img2.shape
    output_image[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]: cols1+translation_dist[0]] = img1


    origin_r = int(points_2[0][0][1])
    origin_c = int(points_2[0][0][0])

    if origin_r < 0:
        origin_r = 0
    if origin_c < 0:
        origin_c = 0

    if new_image[0] > frame_size[0]-origin_r:
        img2 = img2[0:frame_size[0]-origin_r,:]
        
    if new_image[1] > frame_size[1]-origin_c:
        img2 = img2[:,0:frame_size[1]-origin_c]    
            
    output_image[origin_r:new_image[0]+origin_r, origin_c:new_image[1]+origin_c] = img2    
    
    return output_image

def build_mosaic(image_list, save_mosaic_dir, mosaic_base_name, 
                 num_features=10000, reproj_thresh=2.0, flag_save=False):
    avg_error       = []  # list of average reprojection error
    matches_list    = []  # list of number of good matches at every stage
    sift            = cv2.SIFT_create(num_features)
    img_count       = 0
    
    # starting out with first image
    first_image     = cv2.imread(image_list.pop(0))
    height, width   = first_image.shape[:2]
    first_image     = cv2.resize(first_image, (int(width/4), int(height/4)))
    stitched_mosaic = first_image
    img_count       += 1
    if flag_save:
        cv2.imwrite(save_mosaic_dir + mosaic_base_name + str(img_count) + '.png', stitched_mosaic)
    
    
    while image_list:
        image_name = image_list.pop(0)
        img_count  += 1
        print(f'Stitching for image {image_name}')
        image = cv2.imread(image_name)          
        height, width = image.shape[:2]        
        image = cv2.resize(image, (int(width/4), int(height/4)))

        kp1, des1 = sift.detectAndCompute(cv2.cvtColor(stitched_mosaic,cv2.COLOR_BGR2GRAY),None)  
        kp2, des2 = sift.detectAndCompute(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY),None)
 
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)

    
        good       = []
        all_points = []
        for m,n in matches:
            if m.distance < 0.3*n.distance:
                good.append(m)                
            all_points.append(m)        
        matches_list.append(len(good))


        dst_pts = np.float32([kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        src_pts = np.float32([kp2[m.trainIdx].pt for m in good ])              
        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, reproj_thresh)
        
        stitched_mosaic = stitching(stitched_mosaic, image, H)
        if flag_save:
            cv2.imwrite(save_mosaic_dir + mosaic_base_name + str(img_count) + '.png', stitched_mosaic)        
 
        cur_error = reprojection_error(src_pts, dst_pts, H)
        print(f'Current reprojection error {cur_error}')
        avg_error.append(cur_error)
        
    return avg_error

num_imgs_to_use  = 
raw_img_dir      = ''
save_mosaic_dir  = ''
error_data_dir   = ''
mosaic_base_name = 'mosaic_v1'
flag_save        = False           
dataset          = 'city'
ftr_detector     = 'sift'
num_keypoints    = 10000
error_filename   = dataset+'_'+ftr_detector+'_'+str(num_keypoints)+'.pkl'


image_list   = sorted(glob.glob("*.JPG"))

print(image_list)
#if __name__=='__main__':
error = build_mosaic(image_list, save_mosaic_dir, mosaic_base_name, num_features=num_keypoints, flag_save=flag_save)
print(f'Error list {error}')
with open(error_data_dir + error_filename, 'wb') as f:
    pickle.dump(error, f)

print(error)