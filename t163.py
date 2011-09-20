# coding: utf-8

from api import API

class T163API(API):

    def __init__(self, *args, **kwargs):
        super(T163API, self).__init__(*args, **kwargs)

        self.request_token_url = 'http://api.t.163.com/oauth/request_token'
        self.authenticate_url = 'http://api.t.163.com/oauth/authenticate'
#        self.authenticate_url = 'http://api.t.163.com/oauth/authorize'
        self.access_token_url = 'http://api.t.163.com/oauth/access_token'
        self.credentials_url = 'http://api.t.163.com/account/verify_credentials.json'

    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')
        
    def user(self):
        pass

    def credentials(self):
        """
        {
            name: "开放平台"
            location: ""
            id: "2229543033866779776"
            description: ""
            status: {
                id: "8619344141274950063"
                source: "网易微博"
                text: "这是网易微博开放平台"
                created_at: "Fri Jul 16 11:52:45 +0800 2010"
                truncated: false
                in_reply_to_status_id: null
                in_reply_to_user_id: null
                in_reply_to_screen_name: null
                in_reply_to_user_name: null
            }
            screen_name: "openAPI"
            gender: "0"
            friends_count: "0"
            followers_count: "0"
            statuses_count: "1"
            created_at: "Fri Jul 16 11:52:23 +0800 2010"
            favourites_count: "0"
            profile_image_url: "http://126.fm/15fB1f"
            url: ""
            blocking: false
            following: false
            followed_by: false
            verified: false
        }
        """
        user_info = self.get(self.credentials_url)
        return user_info

    def tweet(self, content):
        self.post('http://api.t.163.com/statuses/update.json', {'status': content})
