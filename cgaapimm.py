import requests
import shutil
import facebook
import cv2
from transform import *
from helper import *
import random
import jsonreader
import socialMedia
import sys

FB_REACTS = ["LIKE", "LOVE", "HAHA", "WOW", "SAD", "ANGRY"]


if(len(sys.argv) > 1):
	cfg = jsonreader.Reader(sys.argv[1])
else:
	print("Please provide a configuration file")
	sys.exit(1)
	
socialMedia.FB_TOKEN = cfg["fb_token"]
FILE_HOME = cfg["file_home"]
if(not os.path.exists(FILE_HOME)):
		os.mkdir(FILE_HOME)
STATE_FILE = FILE_HOME + cfg["state_file"]
LAST_IMAGE = FILE_HOME + cfg["image_file"]
BACKUP_IMAGE = FILE_HOME + cfg["backup_image"]
INITIAL_IMAGE = FILE_HOME + cfg["initial_image"]

restricted_transforms = [everything.everythingTransform]
guaranteed_transforms = [addImage.addImageTransform, superimpose.superimposeTransform, drawShape.drawShapeTransform, putText.putTextTransform]

MAX_SIZE = 1024


def main():
	if(not os.path.exists(STATE_FILE)):
		#if there is no state file create an initial post
		initialPost()
		return

	#first, check the results from the last post
	selectedTransforms = {}
	with open(STATE_FILE, 'r') as f:
		temp = f.read().splitlines()
		id = temp[0]
		selectedTransforms["LIKE"] = temp[1]
		selectedTransforms["LOVE"] = temp[2]
		selectedTransforms["HAHA"] = temp[3]
		selectedTransforms["WOW"] = temp[4]
		selectedTransforms["SAD"] = temp[5]
		selectedTransforms["ANGRY"] = temp[6]
	results = socialMedia.fb_get_reacts(id)
	winners = []
	max = -1
	for r in results.items():
		if(r[1] > max):
			winners = [r[0]]
			max = r[1]
		elif(r[1] == max):
			winners.append(r[0])
		else:
			#do nothing
			pass
	
	for w in winners:
		print(w)
	#create backup image, in case something goes wrong
	shutil.copyfile(LAST_IMAGE, BACKUP_IMAGE)
	#retrieve the last image
	image = cv2.imread(LAST_IMAGE)
	
	#choose which transform to use
	alltransforms = abstractTransform.abstractTransformClass.__subclasses__()
	ts = []
	for t in alltransforms:
		for w in winners:
			if (selectedTransforms[w] == t.name()):
				ts.append(t)
	
	if (not ts):
		print("Something went wrong, no transforms found with that name")
		return
	used_t = random.choice(ts)
	print(used_t.name())
	
	#try to apply the transform
	error = False
	try:
		image = used_t.transform(image)
		#resize the image to keep it manageable
		image = resizeImage(image, MAX_SIZE)
		cv2.imwrite(LAST_IMAGE, image)
	except Exception as e:
		print(e, file=sys.stderr)
		error = True
	
	#choose 6 new transform options
	new_ts = []
	new_ts.append(random.choice(guaranteed_transforms))
	while (len(new_ts) < 6):
		t = random.choice(alltransforms)
		if(t in restricted_transforms):
			t = random.choice(alltransforms)
		if(not t in new_ts):
			new_ts.append(t)
			
			
	#post to facebook
	print("Posting Image")
	message = ""
	if(error):
		message = "Something went wrong when applying transform: " + used_t.name() + ". Try again with new transform options."
	else:
		message = "Applied transform: " + used_t.name()
	message = (message
				+ "\nReact to vote for the next transform!"
				+"\n\n👍: " + new_ts[0].name()
				+"\n❤: " + new_ts[1].name()
				+"\n😂: " + new_ts[2].name()
				+"\n😮: " + new_ts[3].name()
				+"\n😢: " + new_ts[4].name()
				+"\n😡: " + new_ts[5].name()
				+"\n\nDescriptions for each transform can be found in the comments below.")
	newId = socialMedia.photo_to_facebook(LAST_IMAGE, message)
	print("Done")
	print("new Id:" + newId)
	
	#post followup comment
	print("Posting Followup Comment")
	followup = ""
	for i, t in enumerate(new_ts):
		followup = followup + FB_REACTS[i] + " - " + t.name() + ":\n" + t.description() + "\n\n"
	socialMedia.fb_comment(newId, followup)
	
	#finally, write the state back to the state file
	print("New options:")
	with open(STATE_FILE, 'w') as f:
		f.write(newId + '\n')
		for t in new_ts:
			print(t.name())
			f.write(t.name() + '\n')


def initialPost():
	print("No state file found, posting initial message and image instead.")
	shutil.copyfile(INITIAL_IMAGE, LAST_IMAGE)
	message = ("Hello and welcome to the Community Guided Abstract Art / Post-Ironic Meme Machine!\n\n" +
				"Here's how this bot works:\n" +
				"We start with an image, and then the community votes on how to transform the image!" +
				"These transforms range from increasing the contrast a little bit, to radial blurring, and a whole lot of other things besides!\n\n" +
				"New transforms are constantly being added, so keep an eye out!\n\n" +
				"With that said, here's the first image!\n")
	alltransforms = abstractTransform.abstractTransformClass.__subclasses__()
	
	new_ts = []
	new_ts.append(random.choice(guaranteed_transforms))
	while (len(new_ts) < 6):
		t = random.choice(alltransforms)
		if(t in restricted_transforms):
			t = random.choice(alltransforms)
		if(not t in new_ts):
			new_ts.append(t)
	message = (message
				+ "\nReact to vote for the next transform!"
				+"\n\n👍: " + new_ts[0].name()
				+"\n❤: " + new_ts[1].name()
				+"\n😂: " + new_ts[2].name()
				+"\n😮: " + new_ts[3].name()
				+"\n😢: " + new_ts[4].name()
				+"\n😡: " + new_ts[5].name()
				+"\n\nDescriptions for each transform can be found in the comments below.")
	print(message)
	newId = socialMedia.photo_to_facebook(INITIAL_IMAGE, message)
	print("Posting Followup Comment")
	followup = ""
	for i, t in enumerate(new_ts):
		followup = followup + FB_REACTS[i] + " - " + t.name() + ":\n" + t.description() + "\n\n"
	socialMedia.fb_comment(newId, followup)
	
	#finally, write the state back to the state file
	print("New options:")
	with open(STATE_FILE, 'w') as f:
		f.write(newId + '\n')
		for t in new_ts:
			print(t.name())
			f.write(t.name() + '\n')

if (__name__ == '__main__'):
	main()
