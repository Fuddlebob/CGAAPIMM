from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class invertColourTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Invert Colours"
	
	def description():
		#return a brief description of what the transform does
		return "Inverts the colours of the image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return cv2.bitwise_not(image)