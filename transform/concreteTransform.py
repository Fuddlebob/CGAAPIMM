from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class concreteTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Name. Must be unique."
	
	def description():
		#return a brief description of what the transform does
		return "Description. Be sure to include punctuation."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return image