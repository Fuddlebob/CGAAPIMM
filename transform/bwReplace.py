from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class bwReplaceTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Black/White Replacement"
	
	def description():
		#return a brief description of what the transform does
		return "Replaces all black or white pixels with new colours."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		black_replace = randomColour()
		white_replace = randomColour()
		image[np.where((image==[0,0,0]).all(axis=2))] = np.asarray(black_replace)
		image[np.where((image==[255,255,255]).all(axis=2))] = np.asarray(white_replace)
		return image