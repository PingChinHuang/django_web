from pprint import pprint
import flickrapi
import webbrowser


class FlickrUtils(object):

    api_key = u'9fb3c52ff07ab22a3126417d5ccb4a23'
    api_secret = u'7a7c897f46e5e421'
    instance = None
    photos_get_methods = None 

    def __init__(self):
        self.instance = flickrapi.FlickrAPI(self.api_key, self.api_secret);
        #if not flickr.token_valid(perms=u'write'):
        #    instance.get_request_token(oauth_callback='oob')
        #    print(flickr.auth_url(perms=u'write'))
        #    verifier = str(input('Verifier code: '))
        #    token = flickr.get_access_token(verifier)
        self.photos_get_methods = {
            'getInfo': self.instance.photos.getInfo,
            'getExif': self.instance.photos.getExif
        }

    def __getattr__(self):
        print(__getattr__)

    def __repr__(self):
        return '%s' % (self.__class__.__name__)

    def __call__(self, reqtype, apitype, method, **kwargs):
        return {
            'get': self.get,
            'set': self.set
        }[reqtype](apitype, method, **kwargs)

    def get(self, apitype, method, **kwargs):
        return {
            'photos': self.photos_get_methods
        }[apitype][method](**kwargs)

    def set(self, apitype, method, **kwargs):
        return None

if __name__ == '__main__':
    f_util = FlickrUtils()
    #resp = f_util.get('photos', 'getInfo', photo_id='36007097620')
    resp = f_util('get', 'photos', 'getInfo', photo_id='36007097620')

    for attr in dir(resp):
        if hasattr(resp, attr):
            print("resp.%s = %s" % (attr, getattr(resp,attr)))

    for child in resp:
        print(child.tag)
        print(child.attrib['id'])

