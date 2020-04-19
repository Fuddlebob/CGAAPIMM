import abc

class abstractTransformClass(object): 
	@staticmethod
	@abc.abstractmethod
	def name():
		#short form name for the transform
		return "Name"
	
	@staticmethod
	@abc.abstractmethod
	def description():
		#return a brief description of what the transform does
		return "Description"
	
	@staticmethod
	@abc.abstractmethod
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return image