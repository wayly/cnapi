# coding: utf-8
from api import API
from django.utils import simplejson
import re

class SinaAPI(API):

    def __init__(self, *args, **kwargs):
        super(SinaAPI, self).__init__(*args, **kwargs)

        self.request_token_url = 'http://api.t.sina.com.cn/oauth/request_token'
        self.authenticate_url = 'http://api.t.sina.com.cn/oauth/authorize'
        self.access_token_url = 'http://api.t.sina.com.cn/oauth/access_token'

    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')
        params['source'] = self.consumer_key

    def _process_access_token(self, result):
        if 'user_id' in result:
            self.user_id = re.search('user_id=(\d+)', result).group(1)

    def credentials(self):
        pass

    def user(self, user_id):
        assert user_id > 0
        return self.get("http://api.t.sina.com.cn/users/show.json", {'user_id':user_id})

    def tweet(self, content, **kw):
        params = dict()
        params['status'] = content
        params['annotations'] = simplejson.dumps(dict(from_baye=True))
        params.update(kw)
        return self.post("http://api.t.sina.com.cn/statuses/update.json",
            params,
        )


    def tweet_pic(self, content, picture):
        params = dict()
        params['status'] = content
        params['annotations'] = simplejson.dumps(dict(from_baye=True))

        filedatas = dict()
        filedatas['pic'] = picture
        return self.post("http://api.t.sina.com.cn/statuses/upload.json", params, filedatas)
    
    def show(self, tweet_id):
        """ 得到微博的信息 """
        msg = self.get("http://api.t.sina.com.cn/statuses/show/%s.json" % tweet_id)
        return msg

    def reply(self, tweet_id, content, cid=None):
        """ 回复微博
        cid 要回复的评论
        """
        assert tweet_id >= 0
        params = dict(id=tweet_id, comment=content)
        if cid:
            params['cid'] = cid
        resp =  self.post("http://api.t.sina.com.cn/statuses/comment.json", params)
        return resp

    def retweet(self, tweet_id, content):
        """转发微博
        content: 转发的内容
        """
        assert tweet_id >= 0
        params = dict(id=tweet_id, status=content, is_comment=1)
        resp = self.post("http://api.t.sina.com.cn/statuses/repost.json",
            params)
        return resp

    def friends(self, user_id):
        """ 得到朋友列表 """
        friends = self.get("http://api.t.sina.com.cn/friends/ids.json", {'user_id':user_id})
        return friends

    def mentions(self, **kwargs):
        tweets = self.get("http://api.t.sina.com.cn/statuses/mentions.json", kwargs)
        return tweets

    def tweets_about_link(self, short_url):
        params = {'url_short': short_url }
        tweets = self.get("http://api.t.sina.com.cn/short_url/share/statuses.json", params)
        return tweets


