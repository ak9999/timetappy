import requests

import datetime
import hashlib
import json


class TimeTapAuthentication(requests.auth.AuthBase):

    def __init__(self, APIKey: str, PrivateKey: str):
        self.APIKey = APIKey
        self.PrivateKey = PrivateKey
        self.timestamp = datetime.datetime.now().timestamp()

    def get_authorization_header(self):
        signature = hashlib.md5((self.APIKey + self.PrivateKey).encode('utf-8')).hexdigest()
        token = requests.get(url=f'https://api.timetap.com/live/sessionToken?apiKey={self.APIKey}&timestamp={self.timestamp}&signature={signature}')
        token = json.loads(token.text)
        return 'Bearer ' + token['sessionToken']

    def __call__(self, request):
        request.headers['Authorization'] = self.get_authorization_header()
        return request
