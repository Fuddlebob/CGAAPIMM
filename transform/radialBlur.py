from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random

class radialBlurTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Radial Blur"
	
	def description():
		#return a brief description of what the transform does
		return "Makes everything funnier."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		#copied this shit from stackoverflow lol
		w, h = image.shape[:2]

		center_x = w / 2
		center_y = h / 2
		blur = random.triangular(0.001, 0.05, 0.01)
		iterations = random.randint(2, 8)

		growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
		shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
		growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
		shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)

		for i in range(iterations):
			tmp1 = cv2.remap(image, growMapx, growMapy, cv2.INTER_LINEAR)
			tmp2 = cv2.remap(image, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR)
			image = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)
		return image