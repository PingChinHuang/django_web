from django.shortcuts import render
from . import flickr_api

# Create your views here.

my_user_id = '45566434@N04'

def index(request):
    flickr = flickr_api.FlickrUtils()
    response = flickr('get', 'photoset', 'getList',
                        user_id=my_user_id, page='1', per_page='10',
                        primary_photo_extras='url_s')
    photoset_list = flickr.parse_photoset_list_response(response)
    return render(request, 'flickr/index.html', {'photoset_list': photoset_list})
