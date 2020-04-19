import requests
import imutils
import cv2
import random
import os
import shutil
import tempfile
#a bunch of common helper functions to be used by transforms

#constants
SPB_API = "https://www.shitpostbot.com/api/randsource"
SPB_IMGROOT = "https://www.shitpostbot.com/"

def img_size(image):
	#returns (height, width) of an openCV image
	w, h = image.shape[1::-1]
	return (h, w)
	
def randomImage():
	#returns an openCV image of a random spb source image
	r= requests.get(SPB_API)
	content = str(r.content)[2:-1:]
	content = content.replace('null', '0')
	sourcename = eval(content)['sub']['img']['full'].replace('\\', '')
	url = SPB_IMGROOT + sourcename
	extension = sourcename.split('.')[-1]
	outname = "test." + extension
	r = requests.get(url, stream=True)
	if r.status_code == 200:
		with open(outname, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
	image = cv2.imread(outname)	
	os.remove(outname)
	return image
	

	
def randomText():
	#returns a random spb source image name
	r= requests.get(SPB_API)
	content = str(r.content)[2:-1:]
	content = content.replace('null', '0')
	return eval(content)['sub']['name']
	
def randomColour():
	#returns a random colour
	return (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))
	
def randomPoint(width, height):
	#returns a random point within a bounds
	return (random.randint(0, width), random.randint(0, height))
	
	
def resizeImage(image, max_size):
	#resizes an image to be less than a certain max size in either direction
	height, width = img_size(image)
	if(height > max_size or width > max_size):
		if(height > width):
			return imutils.resize(image, height=max_size)
		else:
			return imutils.resize(image, width=max_size)
	else:
		return image
		
def refreshImage(image):
	#refreshes the image by saving it and running imread again
	#this often fixes a number of errors caused when running multiple transforms back to back
	tempname = mkstemp(suffix=".png")[1]
	cv2.imwrite(tempname, image)
	image = cv2.imread(tempname)
	os.remove(tempname)
	return image