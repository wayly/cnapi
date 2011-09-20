# coding: utf-8
from api import API
import simplejson
import re

class Twitter(API):

    def __init__(self, *args, **kwargs):
        super(Twitter, self).__init__(*args, **kwargs)
        self.request_token_url = "https://api.twitter.com/oauth/request_token"
        self.authenticate_url = 'https://api.twitter.com/oauth/authorize'
        self.access_token_url = "https://api.twitter.com/oauth/access_token"

    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')
        params['source'] = self.consumer_key

    def _process_result(self, result):
        return simplejson.loads(result)

    def _process_access_token(self, result):
        if 'user_id' in result:
            self.user_id = re.search('user_id=(\w+)', result).group(1)

    def user(self, user_id):
        """ 得到用户信息
        "name": "Twitter API",
        "profile_sidebar_border_color": "87bc44",
        "profile_background_tile": false,
        "profile_sidebar_fill_color": "e0ff92",
        "location": "San Francisco, CA",
        "profile_image_url": "http://a3.twimg.com/profile_images/689684365/api_normal.png",
        "created_at": "Wed May 23 06:01:13 +0000 2007",
        "profile_link_color": "0000ff",
        "favourites_count": 2,
        "url": "http://apiwiki.twitter.com",
        "contributors_enabled": true,
        "utc_offset": -28800,
        "id": 6253282,
        "profile_use_background_image": true,
        "profile_text_color": "000000",
        "protected": false,
        "followers_count": 160752,
        "lang": "en",
        "verified": true,
        "profile_background_color": "c1dfee",
        "geo_enabled": true,
        "notifications": false,
        "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Don't get an answer? It's on my website.",
        "time_zone": "Pacific Time (US & Canada)",
        "friends_count": 19,
        "statuses_count": 1858,
        "profile_background_image_url": "http://a3.twimg.com/profile_background_images/59931895/twitterapi-background-new.png",
        "status": {
          "coordinates": null,
          "favorited": false,
          "created_at": "Tue Jun 22 16:53:28 +0000 2010",
          "truncated": false,
          "text": "@Demonicpagan possible some part of your signature generation is incorrect & fails for real reasons.. follow up on the list if you suspect",
          "contributors": null,
          "id": 16783999399,
          "geo": null,
          "in_reply_to_user_id": 6339722,
          "place": null,
          "source": "<a href="http://www.tweetdeck.com" rel="nofollow">TweetDeck</a>",
          "in_reply_to_screen_name": "Demonicpagan",
          "in_reply_to_status_id": 16781827477
        },
        "screen_name": "twitterapi",
        "following": false
        """
        return self.get("http://api.twitter.com/1/users/show.json",
            {'user_id':user_id})

    def tweet(self, content):
        """ 更新 """
        return self. post("http://api.twitter.com/1/statuses/update.json",
            {'status':content})
