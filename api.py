import urllib
import urllib2
import httplib
import urlparse
import simplejson

from oauth import OAuthConsumer, OAuthRequest, OAuthSignatureMethod_HMAC_SHA1, OAuthToken

def _split_url(url):
    if url.startswith('http://'):
        url = url[7:]
    if url.startswith('https://'):
        url = url[8:]

    items = url.split('/')
    return items[:1][0], "/" + "/".join(items[1:])


class API(object):
    def __init__(self, consumer_key, consumer_secret, callback=''):
        """ """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback = callback
        self.consumer = OAuthConsumer(consumer_key, consumer_secret)
        self.access_token = None
        self.request_token = None

        self.request_token_url = None
        self.access_token_url = None
        self.authenticate_url = None
        self.credentials_url = None

    def _set_access_token(self, access_token):
        if type(access_token) in (str, unicode):
            self._access_token = OAuthToken.from_string(access_token)
        else:
            self._access_token = access_token

    def _get_access_token(self):
        if not self._access_token :
#            raise Exception("api instance not auth yet")
            pass


        return self._access_token

    access_token = property(_get_access_token, _set_access_token)

    def _set_request_token(self, request_token):
        self._request_token = request_token

    def _get_request_token(self):
        if not self._request_token:
            raise Exception("call get_auth_url first")
        return self._request_token

    request_token = property(_get_request_token, _set_request_token)

    def encode_multipart(self, fields, files):
        BOUNDARY = "-.-0.0-.-"
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.iteritems():
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value[0])
        for (key, value) in files.items():
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key))
            L.append('Content-Type: %s' % "application/octet-stream")
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_auth_url(self):
        """ """
        request = OAuthRequest.from_consumer_and_token(
            self.consumer,
            http_url = self.request_token_url,
            callback = self.callback)

        request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), self.consumer, None)
        resp = urllib2.urlopen(urllib2.Request( request.to_url()))
        token = resp.read()
        request_token = OAuthToken.from_string(token)
        self.request_token = request_token

        request = OAuthRequest.from_token_and_callback(
            token=request_token, http_url=self.authenticate_url,
            callback = self.callback
            )
        return request.to_url()

    def auth(self, request_token, verifier):
        self.request_token = OAuthToken.from_string(request_token)
        request = OAuthRequest.from_consumer_and_token(
            self.consumer,
            token=self.request_token,
            http_url=self.access_token_url,
            verifier=str(verifier)
        )
        request.sign_request(
            OAuthSignatureMethod_HMAC_SHA1(),
            self.consumer,
            self.request_token
            )

        #if mode == 'header':
        #    resp = urllib2.urlopen(urllib2.Request(url, headers=request.to_header()))
        #else:
        #    resp = urllib2.urlopen(urllib2.Request(request.to_url()))
        resp = urllib2.urlopen(urllib2.Request(request.to_url()))
        string = resp.read()
        access_token = OAuthToken.from_string(string)
        self.access_token = access_token
        self._process_access_token(string)

    def http(self, method, url, params, filedatas=None):
        headers = {}
        headers.setdefault('User-Agent', "BAYE.ME social comment")
#        headers.setdefault("Accept", "text/html")

        self._process_params(params)
        request = OAuthRequest.from_consumer_and_token(
            self.consumer,
            http_url=url,
            http_method=method,
            token=self.access_token,
            parameters=params
        )
        request.sign_request(
            OAuthSignatureMethod_HMAC_SHA1(), self.consumer,
            self.access_token
        )
        if method == 'POST':
            url = request.get_normalized_http_url()
        else:
            url = request.to_url()
        signed_params = request.to_postdata()

        if filedatas:
            _params = urlparse.parse_qs(signed_params, keep_blank_values=True)
            content_type, body = self.encode_multipart(_params, filedatas)
        else:
            content_type, body = "application/x-www-form-urlencoded", signed_params
        headers.setdefault("Content-Type", content_type)

        host, path = _split_url(url)
        conn = httplib.HTTPConnection(host)
        conn.request(method, path, body, headers)
        resp = conn.getresponse()
        json =  resp.read()
        conn.close()
        return self._process_result(json)

    def get(self, url, params={}):
        assert url != None
        return self.http("GET", url, params)

    def post(self, url, params, filedatas=None):
        assert url != None
        return self.http('POST', url, params, filedatas)

    def execute(self, url, params, consumer, access_token, method='POST', mode='header'):
        headers = {}
        headers.setdefault('User-Agent', "python")
        headers.setdefault("Accept", "text/html")
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

        request = OAuthRequest.from_consumer_and_token(
            self.consumer,
            http_url=url,
            http_method=method,
            token=access_token,
            parameters=params,
        )
        request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), consumer, access_token)
        if mode == 'header':
            headers.update(request.to_header())
        else:
            url = request.get_normalized_http_url()
            params = request.to_postdata()
        multipart_encode({})
        host, path = _url_spllit(url)
        conn = httplib.HTTPConnection(host)

        conn.request(method, path, params, headers)
        resp = conn.getresponse()
        json = resp.read()
        conn.close()
        return json

    def credentials(self):
        return self.get(self.credentials_url)

    def user(self):
        raise Exception("Not implemented")

    def tweet(self, content):
        raise Exception("Not implemented")

    def tweet_pic(self, content, picture):
        raise Exception("Not implemented")

    def show(self, tweet_id):
        raise Exception("Not implemented")

    def friends(self):
        raise Exception("Not implemented")

    def reply(self, tweet_id, content):
        raise Exception("Not implemented")

    def retweet(self, tweet_id, content):
        raise Exception("Not implemented")

    def mentions(self):
        raise Exception("Not implemented")

    def _process_params(self, params):
        pass

    def _process_result(self, result):
        return simplejson.loads(result)

    def _process_access_token(self, result):
        pass
