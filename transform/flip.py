from . import abstractTransform
import cv2
import numpy as np
import random

class flipTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Flip"
	
	def description():
		#return a brief description of what the transform does
		return "Flips the image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		flip = random.randint(0, 1)
		return cv2.flip(image, flip)