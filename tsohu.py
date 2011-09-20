# coding: utf-8

from cnapi.api import API

class SohuAPI(API):
    def __init__(self, *args, **kwargs):
        super(SohuAPI, self).__init__(*args, **kwargs)
        self.request_token_url = "http://api.t.sohu.com/oauth/request_token"
        self.access_token_url = "http://api.t.sohu.com/oauth/access_token"
        self.authenticate_url = "http://api.t.sohu.com/oauth/authorize"
        self.credentials_url = "http://api.t.sohu.com/account/verify_credentials.json"
        
    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')

    def credentials(self):
        """
        {"id":"11104",
        "screen_name":"ss",
        "name":"",
        "location":"",
        "description":"上班时代是吃快餐的时代",
        "url":"",
        "gender":1,
        "profile_image_url":"http://1811.img.pp.sohu.com.cn/images/blog/2010/3/18/9/26/12820f76790g189_0.jpg",
        "protected":false,
        "followers_count":36,
        "profile_background_color":"",
        "profile_text_color":"",
        "profile_link_color":"",
        "profile_sidebar_fill_color":"",
        "profile_sidebar_border_color":"",
        "friends_count":30,
        "created_at":"Tue Dec 15 10:15:50 +0800 2009",
        "favourites_count":0,
        "utc_offset":"",
        "time_zone":"",
        "profile_background_image_url":"",
        "notifications":"",
        "geo_enabled":false,
        "statuses_count":685,
        "following":true,
        "verified":false,
        "lang":"GBK",
        "contributors_enabled":false}
        """
        return self.get(self.credentials_url)

    def tweet(self, content):
        self.post('http://api.t.sohu.com/statuses/update.json', {'status': content})
