import flickrapi
import webbrowser

class Photoset:
    def __init__(self, id, title, photos, primary_photo_url, w, h):
        self._id = id
        self._title = title
        self._photos = photos
        self._primary_photo_url = primary_photo_url
        self._width = w
        self._height = h

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

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
    
class Photo:
    def __init__(self, id, title, url, w, h):
        self._id = id
        self._title = title
        self._url = url
        self._width = w
        self._height = h

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

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
        self.photos_methods = {
            'getInfo': self.instance.photos.getInfo,
            'getExif': self.instance.photos.getExif,
            'addTags': self.instance.photos.addTags,
            'removeTags': self.instance.photos.removeTags,
        }

        self.photoset_methods = {
            'getList': self.instance.photosets.getList,
            'getPhotos': self.instance.photosets.getPhotos
        }
        
        self.tags_methods = {
            'getListPhoto': self.instance.tags.getListPhoto,
        }

    def __getattr__(self):
        print(__getattr__)

    def __repr__(self):
        return '%s' % (self.__class__.__name__)

    def __call__(self, reqtype, apitype, method, **kwargs):
        return {
            'call': self.call,
        }[reqtype](apitype, method, **kwargs)

    def call(self, apitype, method, **kwargs):
        return {
            'photos': self.photos_methods,
            'photoset': self.photoset_methods,
            'tags': self.tags_methods,
        }[apitype][method](**kwargs)

    def parse_photoset_list_response(self, root):
        photoset_list = []
        if root == None or root.attrib['stat'] != 'ok' :
            return None

        photosets = root.find('photosets')
        if photosets == None :
            return None
        
        print("Total pages: {}, current page: {}".format(photosets.attrib['pages'], photosets.attrib['page']))
        
        for photoset in photosets.findall('photoset'):
            print(photoset.tag, photoset.attrib)
            for child in photoset:
                print(child.tag, child.attrib, child.text)
                
                import re
                urlRe = re.compile('url.*')
                heightRe = re.compile('height.*')
                widthRe = re.compile('width.*')
                primary_photo_url = '' 
                id = ''
                title = ''
                w = ''
                h = ''

                primary_photo_obj = photoset.find('primary_photo_extras')
                if primary_photo_obj == None:
                    continue

                id = photoset.attrib['id']
                for key in primary_photo_obj.attrib:
                    if urlRe.match(key):
                        primary_photo_url = primary_photo_obj.attrib[key]
                    elif heightRe.match(key):
                        h = primary_photo_obj.attrib[key]
                    elif widthRe.match(key):
                        w = primary_photo_obj.attrib[key]


                if photoset.find('title') != None:
                    title = photoset.find('title').text

                photoset_obj = Photoset(id,
                                        title,
                                        photoset.attrib['photos'],
                                        primary_photo_url, w, h)
            
            photoset_list.append(photoset_obj)

        return photoset_list, photosets.attrib['pages'], photosets.attrib['page']
    
    def parse_get_photos_response(self, root):
        photo_list = []
        if root == None or root.attrib['stat'] != 'ok' :
            return None

        photoset = root.find('photoset')
        if photoset == None :
            return None
        
        print("Total pages: {}, current page: {}".format(photoset.attrib['pages'], photoset.attrib['page']))
        
        for photo in photoset.findall('photo'):
            print(photo.tag, photo.attrib)
                
            import re
            urlRe = re.compile('url.*')
            heightRe = re.compile('height.*')
            widthRe = re.compile('width.*')
            url = '' 
            id = ''
            title = ''
            w = ''
            h = ''

            id = photo.attrib['id']
            title = photo.attrib['title']
            for key in photo.attrib:
                if urlRe.match(key):
                    url = photo.attrib[key]
                elif heightRe.match(key):
                    h = photo.attrib[key]
                elif widthRe.match(key):
                    w = photo.attrib[key]

            photo_obj = Photo(id, title, url, w, h)
            photo_list.append(photo_obj)

        return photo_list, photoset.attrib['id'], photoset.attrib['pages'], photoset.attrib['page'], photoset.attrib['title']
    
    def parse_get_tags_response(self, root):
        tag_list = []
        if root == None or root.attrib['stat'] != 'ok' :
            return None

        photo = root.find('photo')
        if photo == None :
            return None
        
        tags = photo.find('tags')
        if tags == None :
            return None
        print(photo.attrib['id'])

        for tag in tags:
            print('tag: {}'.format(tag.attrib['raw']))
            tag_list.append('#' + tag.attrib['raw'])
        
        return tag_list
    
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
