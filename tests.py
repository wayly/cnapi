import unittest
import urllib2
import sina, qq

def test_sina_api():
    api = sina.SinaAPI("1886914172", "acf161b562c77993170a8128c4b0ad3c")
#    print api.get_auth_url()
#    request_token = api.request_token
#    verifier = raw_input("PIN: ")
#    api.auth(request_token, verifier)
#    api.tweet("test wrapper class")
    #api.get_friends()
    api.access_token = u'oauth_token_secret=4da3dfd1f3dc71355f8b9a50b748d295&oauth_token=68982e9fd783ddedd4d0178066e61ea8'
    tweets = api.tweets_about_link("http://t.cn/aK05eO")
    print tweets
#    for status in tweets['share_statuses']:
#        print status['user']['name']
#        print status['source']
#        print status['text']
    #pic = urllib2.urlopen("http://img3.douban.com/mpic/s6809577.jpg").read()
    #print api.tweet_pic("test picture", pic)
    #print "finished tweet picture"

def test_qq_api():
    api = qq.TxAPI("ea9392a3df5a43c68dab8a26e5726575", "1b3ad3b2094c014cab81fbfe3b73b139",
        callback="http://localhost:8000")
    print api.get_auth_url()
    request_token = api.request_token
    verifier = raw_input("PIN: ")
    api.auth(request_token, verifier)
    api.tweet("test wrapper class")


test_sina_api()
