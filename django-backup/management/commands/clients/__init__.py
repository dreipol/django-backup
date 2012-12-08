__author__ = 'phil'
import pickle
import os
from dropbox import client, rest, session
from dropbox.client import DropboxClient

class DropboxBackupClient(object):


	def __init__(self, key,secret,type, token_path):
		self.TOKENS_FILEPATH = token_path
		self.session = session.DropboxSession(key, secret, type)


	def check_for_authorization(self):
		try:
			if os.path.exists(self.TOKENS_FILEPATH):
				with open(self.TOKENS_FILEPATH, 'rb') as tokenhandle:
					tokendata = pickle.load(tokenhandle)
				self.request_token = tokendata.get('request_token')
				self.access_token = tokendata.get('access_token')
				self.session.set_token(self.access_token.key, self.access_token.secret)
				self.client = DropboxClient(self.session)
				self.client.account_info()
				return True
			else:
				self.get_authorization()
		except Exception:
			return False
		return True

	def prompt_for_authorization(self):
		print  "Dropbox not authorized, visit the following URL to authorize %s and press Enter to continue" % self.session.build_authorize_url(self.request_token)
		raw_input()
		self.access_token = self.session.obtain_access_token(self.request_token)
		self.tokendata = dict(request_token=self.request_token, access_token=self.access_token)
		with open(self.TOKENS_FILEPATH, 'wb') as tokenhandle:
			pickle.dump(self.tokendata, tokenhandle, -1)




	def get_authorization(self):
		self.request_token = self.session.obtain_request_token()
		self.authorize_url = self.session.build_authorize_url(self.request_token)
		self.prompt_for_authorization()
		self.client = DropboxClient(self.session)
		self.client.account_info()


	def upload_file(self, file_object, upload_target):
		if self.check_for_authorization():
			self.client.put_file(upload_target, file_object)
