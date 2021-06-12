import numpy as np
from scipy import ndimage as nd
from skimage.feature import hog
from skimage.filters import roberts, sobel, scharr, prewitt, threshold_otsu, threshold_multiotsu
import skimage.segmentation

from matplotlib import pyplot as plt
import cv2
import math

DEBUG = True

filepath = "./frames/"

def resize(img):
	height, width, channels = img.shape
	dimensions = (width//4, height//4)
	img = cv2.resize(img, dimensions, interpolation = cv2.INTER_AREA)
	return img

def hog_filter(img, orient, radius):
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	fd, hog_image = hog(img_gray, orientations=8, pixels_per_cell=(radius, radius), cells_per_block=(1, 1), visualize=True)
	return hog_image

if __name__ == '__main__' and DEBUG:
	file1 = "frame0.png"
	file2 = "frame1.png"
	file3 = "frame2.png"

	img = cv2.imread(filepath+file1)
	img = resize(img)
	cv2.imshow("img", img)
	output_img = hog_filter(img, 8, 10)
	cv2.imshow("hog_filter", output_img)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows