import requests
import time
import json
import base64
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.parse import urlparse


class Base(object):

    __access_token_url = 'https://aip.baidubce.com/oauth/2.0/token'

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_obj = {}
        self.__connect_timeout = 60.0
        self.__socket_timeout = 60.0

    def _auth(self, refresh=False):
        if not refresh:
            tm = self._auth_obj.get("time", 0) + int(self._auth_obj.get('expires_in', 0)) - 30
            if tm > int(time.time()):
                return self._auth_obj

        obj = requests.get(self.__access_token_url,
                           verify=False,
                           params={
                               'grant_type': 'client_credentials',
                               'client_id': self._client_id,
                               'client_secret': self._client_secret},
                           timeout=(
                               self.__connect_timeout,
                               self.__socket_timeout)).json()

        obj['time'] = int(time.time())
        self._auth_obj = obj
        return obj

    def _request(self, url, data, headers=None):
        try:
            auth_obj = self._auth()
            params = self._get_params(auth_obj)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(url=url,
                                     data=data,
                                     params=params,
                                     verify=False,
                                     headers=headers,
                                     timeout=(
                                         self.__connect_timeout,
                                         self.__socket_timeout,
                                     ))
            obj = json.loads(response.content.decode())

            if obj.get('error_code', '') == 110:
                auth_obj = self._auth(True)
                params = self._get_params(auth_obj)
                response = requests.post(url=url,
                                         data=data,
                                         params=params,
                                         verify=False,
                                         headers=headers,
                                         timeout=(
                                             self.__connect_timeout,
                                             self.__socket_timeout,
                                         ))
                obj = json.loads(response.content.decode())
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_code': 'SDK108',
                'error_msg': 'connection or read data timeout',
            }

        return obj

    def _get_params(self, auth_obj):
        params = {'access_token': auth_obj['access_token']}
        return params

    def get_auth_obj(self):
        return self._auth_obj



