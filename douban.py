# coding: utf-8
from api import API
import simplejson
import re

class Douban(API):

    def __init__(self, *args, **kwargs):
        super(Douban, self).__init__(*args, **kwargs)
        self.request_token_url = "http://www.douban.com/service/auth/request_token"
        self.authenticate_url = "http://www.douban.com/service/auth/authorize"
        self.access_token_url = "http://www.douban.com/service/auth/access_token"
        self.method = 'headers' 

    def _process_params(self, params):
        params['alt'] = 'json'

    def _process_result(self, result):
        return simplejson.loads(result)

    def _process_access_token(self, result):
        if 'douban_user_id' in result:
            self.user_id = re.search('douban_user_id=(\w+)', result).group(1)
    
    def user(self):
        """ """
        return self.get("http://api.douban.com/people/@me")
