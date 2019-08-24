from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag
import hashlib
from .forms import *

# Create your views here.


def image_placeholder_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(image_placeholder_etag)
def image_placeholder(request, width, height):

    form = ImageForm({'width': width, 'height': height})
    if form.is_valid():

        image = form.generate()

        return HttpResponse(image, content_type='image/png')
    else:
        return doc(request)
        #return HttpResponseBadRequest('Invalid Image Request')
    #return render(request, 'index3.html', context={})


def doc(request):
    example = reverse('placeholder', kwargs={'width': 50, 'height':50})
    context = {
        'example': request.build_absolute_uri(example)
    }
    return render(request, 'doc.html', context)
