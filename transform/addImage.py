from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random
import os
import shutil


class addImageTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Add Image"
	
	def description():
		#return a brief description of what the transform does
		return "Grabs a random shitpostbot5000 source, and places it somewhere on the image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image) 
		newImage = randomImage()
		image = refreshImage(image)
		h1, w1 = img_size(image)
		h2, w2 = img_size(newImage)
		flag = False
		while(not flag):
			tar = random.uniform(0.4, 0.8)
			if (h1 < w1):
				th = h1 * tar
				tw = (th/h2) * w2
				if(th <= h1 and tw <= w1):
					flag = True
			else:
				tw = w1 * tar
				th = *t2/w2) * h2
				if(th <= h1 and tw <= w1):
					flag = True
		h2 = int(th)
		w2 = int(tw)
		newImage = cv2.resize(newImage, (w2, h2), interpolation = cv2.INTER_AREA)
		
		y_offset = random.randint(0, h1-h2)
		x_offset = random.randint(0, w1-w2)
		
		y1, y2 = y_offset, y_offset + h2
		x1, x2 = x_offset, x_offset + w2
		image[y1:y2, x1:x2] = newImage
		return image