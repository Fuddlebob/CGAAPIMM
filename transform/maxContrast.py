from . import abstractTransform
import cv2
import numpy as np
import sys

class maxContrastTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Max Contrast"
	
	def description():
		#return a brief description of what the transform does
		return "Increases the contrast by a ridiculous amount. Like, way more than is ever necessary."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return image * 1000