from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class blurTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Blur"
	
	def description():
		#return a brief description of what the transform does
		return "Blurs the image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		blur_size = (random.randint(4, 40) * 2) + 1
		return cv2.blur(image, (blur_size, blur_size))