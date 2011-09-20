# coding: utf-8

from cnapi.api import API

class KaixinAPI(API):
    def __init__(self, *args, **kwargs):
        super(KaixinAPI, self).__init__(*args, **kwargs)
        self.request_token_url = "http://api.kaixin001.com/oauth/request_token"
        self.authenticate_url = "http://api.kaixin001.com/oauth/authorize"
        self.access_token_url = "http://api.kaixin001.com/oauth/access_token"
        self.credentials_url = "http://api.kaixin001.com/users/me.json"

    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')

    def credentials(self):
        """
        {
            "uid": "46765",
            "name": "刘一",
            "gender": "0",
            "hometown": "北京",
            "city": "北京",
            "status": "2",
            "logo120": "http://pic1.kaixin001.com.cn/logo/4/67/120_46765_2.jpg",
            "logo50": "http://pic1.kaixin001.com.cn/logo/4/67/50_46765_2.jpg",
            "birthday": "80后1月1日",
            "bodyform": "0",
            "blood": "1",
            "marriage": "1",
            "trainwith": "迈克尔 乔丹",
            "interest": "打篮球",
            "favbook": "武侠小说",
            "favmovie": "美国大片",
            "favtv": "美剧",
            "idol": "迈克尔 乔丹",
            "motto": "成功没有捷径",
            "wishlist": "买套房子",
            "intro": "我是一个纯粹的人,一个高尚的人,一个脱离低级趣味的人..",
            "education": [{
                "schooltype": "0",
                "school": "北京大学",
                "class": "软件与微电子学院 11",
                "year": "2011"
            }],
            "career": [{
                "company": "开心网",
                "dept": "技术",
                "beginyear": "2011",
                "beginmonth": "01",
                "endyear": "2011",
                "endmonth": "12"
            }],
            "isStar": "0"
        }
        """
        params = {'fields': 'uid,name,gender,hometown,city,status,logo120,logo50,birthday,bodyform,blood,marriage,trainwith,interest,favbook,favmovie,favtv,idol,motto,wishlist,intro,education,schooltype,school,class,year,career,company,dept,beginyear,beginmonth,endyear,endmonth,isStar'}
        return self.get(self.credentials_url, params)

#    def tweet(self, content):
#        self.post('http://api.t.sohu.com/statuses/update.json', {'status': content})
