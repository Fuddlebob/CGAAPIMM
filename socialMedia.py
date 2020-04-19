import requests
import os
from requests_oauthlib import OAuth1
import time

FACEBOOK_VIDEO_ENDPOINT_URL = 'https://graph-video.facebook.com/me/videos'
FACEBOOK_PHOTO_ENDPOINT_URL = 'https://graph.facebook.com/me/photos'
FB_REACTS = ["LIKE", "LOVE", "HAHA", "WOW", "SAD", "ANGRY"]

TWITTER_MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

TW_OAUTH=None
FB_TOKEN=None

#uploads a video to facebook and returns the id of the post
def video_to_facebook(vidname, message):
	files={'file':open(vidname,'rb')}
	params = (
		('access_token', FB_TOKEN),
		('description', message)
	)	
	response = requests.post(FACEBOOK_VIDEO_ENDPOINT_URL, params=params, files=files)
	print(str(response.content))
	return response.json()["id"]
	
#uploads a photo to facebook and returns the id of the post
def photo_to_facebook(filepath, message):
	print(message)
	files={'file':open(filepath,'rb')}
	params = (
		('access_token', FB_TOKEN),
		('message', message)
	)	
	response = requests.post(FACEBOOK_PHOTO_ENDPOINT_URL, params=params, files=files)
	print(str(response.content))
	return response.json()["id"]
	
#uploads a comment to a post given by postId, with message
def fb_comment(postid, message):
	url = "https://graph.facebook.com/v6.0/" + str(postid) + "/comments"
	
	params = (
		('access_token', FB_TOKEN),
		('message', message)
	)
	response = requests.post(url, params=params)
	print (str(response.content))

#looks up the total number of reacts for a post, and returns a dict of each react and how many they had
def fb_get_reacts(postId):
	results = {}
	for r in FB_REACTS:
		params = (
			('access_token', FB_TOKEN),
			('fields', 'reactions.type('+r+').limit(0).summary(total_count)')
		)
		response = requests.get("https://graph.facebook.com/" + postId, params = params)
		numR = (int) (eval(response.content)['reactions']['summary']['total_count'])
		results[r] = numR
		
	return results
	
	
#uploads a video to twitter
def upload_to_twitter(vidname, message):
	videoTweet = VideoTweet(vidname)
	videoTweet.upload_init()
	videoTweet.upload_append()
	videoTweet.upload_finalize()
	videoTweet.tweet(message)

class VideoTweet(object):

	def __init__(self, file_name):
		'''
		Defines video tweet properties
		'''
		self.video_filename = file_name
		self.total_bytes = os.path.getsize(self.video_filename)
		self.media_id = None
		self.processing_info = None


	def upload_init(self):
		'''
		Initializes Upload
		'''
		print('INIT')

		request_data = {
			'command': 'INIT',
			'media_type': 'video/mp4',
			'media_category': 'TweetVideo',
			'total_bytes': self.total_bytes
		}

		req = requests.post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, auth=TW_OAUTH)
		media_id = req.json()['media_id']

		self.media_id = media_id

		print('Media ID: %s' % str(media_id))


	def upload_append(self):
		'''
		Uploads media in chunks and appends to chunks uploaded
		'''
		segment_id = 0
		bytes_sent = 0
		file = open(self.video_filename, 'rb')

		while bytes_sent < self.total_bytes:
			chunk = file.read(4*1024*1024)
			
			print('APPEND')

			request_data = {
				'command': 'APPEND',
				'media_id': self.media_id,
				'segment_index': segment_id
			}

			files = {
				'media': chunk
			}

			req = requests.post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=TW_OAUTH)

			if req.status_code < 200 or req.status_code > 299:
				print(req.status_code)
				print(req.text)
				sys.exit(0)

			segment_id = segment_id + 1
			bytes_sent = file.tell()

			print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

		print('Upload chunks complete.')


	def upload_finalize(self):
		'''
		Finalizes uploads and starts video processing
		'''
		print('FINALIZE')

		request_data = {
			'command': 'FINALIZE',
			'media_id': int(self.media_id)
		}

		req = requests.post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, auth=TW_OAUTH)
		print(req.json())

		self.processing_info = req.json().get('processing_info', None)
		self.check_status()


	def check_status(self):
		'''
		Checks video processing status
		'''
		request_params = {
			'command': 'STATUS',
			'media_id': int(self.media_id)
		}
		
		req = requests.get(url=TWITTER_MEDIA_ENDPOINT_URL, params=request_params, auth=TW_OAUTH)
		
		processing_info = req.json().get('processing_info', None)
		
		if processing_info is None:
			return

		state = processing_info['state']
		if state == u'succeeded':
			return
		if state == u'failed':
			return
		check_after_secs = processing_info['check_after_secs']
		
		time.sleep(check_after_secs)
		
		self.check_status()


	def tweet(self, message):
		'''
		Publishes Tweet with attached video
		'''
		request_data = {
			'status': message,
			'media_ids': self.media_id
		}
		req = requests.post(url=POST_TWEET_URL, data=request_data, auth=TW_OAUTH)
