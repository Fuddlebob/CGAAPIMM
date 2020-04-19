from . import abstractTransform
import cv2
import numpy as np
import sys

class highContrastTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "High Contrast"
	
	def description():
		#return a brief description of what the transform does
		return "Increases the contrast by a large amount."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return image * 10