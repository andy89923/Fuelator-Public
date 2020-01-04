
from imgurpython import ImgurClient
import json

class ImageHandler():
	_client_id = None
	_client_secret = None

	def __init__(self):
		data = open('info.json')
		js = json.load(data)

		self._client_id = js['client_id']
		self._client_secret = js['client_secret']

		return

	def upload(self, img_path):
		client = ImgurClient(self._client_id, self._client_secret)
		image = client.upload_from_path(img_path, config = {}, anon = False)

		return image['link']

