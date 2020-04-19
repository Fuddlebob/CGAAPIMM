from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class recursionTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Recursion"
	
	def description():
		#return a brief description of what the transform does
		return "Did you mean Recursion?"
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		#define a region of the image
		h, w = img_size(image)
		scale = random.uniform(0.4, 0.8)
		hs = int(h * scale)
		ws = int(w * scale)
		x, y = randomPoint(w - ws, h - hs)
		num_recursions = random.randint(3, 20)
		for i in range(num_recursions):
			scaledImage = cv2.resize(image, (ws, hs), interpolation = cv2.INTER_AREA)
			image[y:y+hs, x:x+ws] = scaledImage
		
		return image