# coding: utf-8
from api import API
import re

class QQAPI(API):

    def __init__(self, *args, **kwargs):
        super(QQAPI, self).__init__(*args, **kwargs)

        self.request_token_url = "https://open.t.qq.com/cgi-bin/request_token"
        self.authenticate_url = 'https://open.t.qq.com/cgi-bin/authorize'
        self.access_token_url = 'https://open.t.qq.com/cgi-bin/access_token'

    def _process_params(self, params):
        for key, value in params.items():
            if type(value) == unicode:
                params[key] = value.encode('utf-8')
        params['format'] = 'json'


    def _process_access_token(self, result):
        if 'name' in result:
            self.user_id = re.search('name=(\w+)', result).group(1)

    def user(self):
        """ 得到用户本人信息
        name: 用户帐户名
        nick: 用户昵称
        uid: 用户id(目前为空)
        head: 头像URL
        location: 所在地
        Isvip: 是否认证用户
        isent: 是否企业机构
        introduction: 个人介绍
        verifyinfo: 认证信息
        birth_year: 出生年
        birth_month:出生月
        birth_day:出生天
        country_code: 国家ID,
        province_code: 地区ID,
        city_code: 城市ID,
        sex:用户性别 1男 2 女 0未知
        fansnum:听众数
        idolnum:收听的人数
        tweetnum:发表的微博数
        tag:
            id:个人标签ID
                name:标签名
        """
        return self.get("http://open.t.qq.com/api/user/info")

    def tweet(self, content):
        return self.post("http://open.t.qq.com/api/t/add",
                {'content': content}
            )

