
import numpy as np
from scipy import ndimage as nd
from skimage import img_as_float
from skimage.filters import roberts, sobel, scharr, prewitt, threshold_otsu, threshold_multiotsu
from skimage.feature import peak_local_max
from skimage.exposure import rescale_intensity
import skimage.segmentation

from matplotlib import pyplot as plt
import cv2
import math

DEBUG = True

filepath = "./Testing/"

if __name__ == '__main__' and DEBUG:
	# file1 = "frame77.jpg"
	# file2 = "frame79.jpg"
	# file3 = "frame81.jpg"
	# file4 = "frame83.jpg"
	# file5 = "frame65.jpg"