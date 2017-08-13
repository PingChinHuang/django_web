import flickrapi
import webbrowser

class Photoset:
    def __init__(self, id, title, photos, primary_photo_url):
        self._id = id
        self._title = title
        self._photos = photos
        self._primary_photo_url = primary_photo_url

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def photos(self):
        return self._photos

    @property
    def primary_photo_url(self):
        return self._primary_photo_url

class FlickrUtils(object):

    api_key = u'9fb3c52ff07ab22a3126417d5ccb4a23'
    api_secret = u'7a7c897f46e5e421'

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

        self.photoset_get_methods = {
            'getList': self.instance.photosets.getList        
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
            'photos': self.photos_get_methods,
            'photoset': self.photoset_get_methods
        }[apitype][method](**kwargs)

    def set(self, apitype, method, **kwargs):
        return None

    def parse_photoset_list_response(self, root):
        photoset_list = []
        if root == None or root.attrib['stat'] != 'ok' :
            return None

        photosets = root.find('photosets')
        if photosets == None :
            return None

        for photoset in photosets.findall('photoset'):
            print(photoset.tag, photoset.attrib)
            for child in photoset:
                print(child.tag, child.attrib, child.text);
                
                import re
                urlRe = re.compile('url.*')
                primary_photo_url = ''
                id = ''
                title = ''

                primary_photo_obj = photoset.find('primary_photo_extras')
                if primary_photo_obj == None:
                    continue

                id = photoset.attrib['id']
                for key in primary_photo_obj.attrib:
                    if urlRe.match(key):
                        primary_photo_url = primary_photo_obj.attrib[key]

                if photoset.find('title') != None:
                    title = photoset.find('title').text

                photoset_obj = Photoset(id,
                                        title,
                                        photoset.attrib['photos'],
                                        primary_photo_url)
            
            photoset_list.append(photoset_obj)

        return photoset_list

if __name__ == '__main__':
    f_util = FlickrUtils()
    #resp = f_util.get('photos', 'getInfo', photo_id='36007097620')
    resp = f_util('get', 'photos', 'getInfo', photo_id='36007097620')
    photosets = f_util('get', 'photoset', 'getList', 
                        user_id='45566434@N04', page='1', per_page='10',
                        primary_photo_extras='url_m')
    """
    for attr in dir(resp):
        if hasattr(resp, attr):
            print("resp.%s = %s" % (attr, getattr(resp,attr)))

    for child in resp:
        print(child.tag)
        print(child.attrib['id'])
    """
    print(photosets.getchildren()[0].attrib)
    """
    for photoset in photosets.getchildren()[0].getchildren():
        print(photoset.tag, photoset.attrib)
        for child in photoset:
            print(child.tag, child.attrib, child.text);
    """

    photoset_list = f_util.parse_photoset_list_response(photosets)
    for photoset in photoset_list:
        print (photoset.primary_photo_url)
        print (photoset.id)
        print (photoset.title)
        print (photoset.photos)
