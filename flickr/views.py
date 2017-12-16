from django.shortcuts import render
from django.http import JsonResponse
from django.template.context_processors import csrf
from . import flickr_api

# Create your views here.

my_user_id = '45566434@N04'

def index(request):
    return render(request, 'flickr/index.html')

def photosets(request, page = 1):
    print("num {}".format(page))
    flickr = flickr_api.FlickrUtils()
    response = flickr('call', 'photoset', 'getList',
                        user_id=my_user_id, page=page, per_page='10',
                        primary_photo_extras='url_m')
    photoset_list, pages, page = flickr.parse_photoset_list_response(response)
    return render(request, 'flickr/photosets.html', {'photoset_list': photoset_list, 'pages': int(pages), 'page': int(page)})    

def photoset(request, setid, page = 1):
    print("setid {}, page {}".format(setid, page))
    flickr = flickr_api.FlickrUtils()
    response = flickr('call', 'photoset', 'getPhotos',
                        user_id=my_user_id, page=page, per_page='50',
                        extras='url_m', photoset_id=setid)
    print(response)
    photo_list, setid, pages, page, title = flickr.parse_get_photos_response(response)
    return render(request, 'flickr/photoset.html', {'photo_list': photo_list, 'pages': int(pages), 'page': int(page), 'setid': int(setid), 'title': title})

def photo_tags_add(request, photoid):
    print("photo id {}".format(photoid))
    return JsonResponse({'status': 'pass'})

def photo_tags_get(request, photoid):
    print("photo id {}".format(photoid))
    flickr = flickr_api.FlickrUtils()
    response = flickr('call', 'tags', 'getListPhoto',photo_id=photoid)
    print(response)    
    tags = flickr.parse_get_tags_response(response)
    print(tags);
    return JsonResponse({'status': 'pass', 'tags': tags})

def photo_tags_remove(request, photoid):
    print("photo id {}".format(photoid))
    return JsonResponse({'status': 'pass'})