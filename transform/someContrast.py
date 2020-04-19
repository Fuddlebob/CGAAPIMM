from . import abstractTransform
import cv2
import numpy as np
import sys

class someContrastTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Contrast"
	
	def description():
		#return a brief description of what the transform does
		return "Increases the contrast. Pretty self explanatory."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return image * 4