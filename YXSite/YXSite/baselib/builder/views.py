from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from django.template import Template, Context
from django.template.loader_tags import BlockNode
from django.conf import settings
from django.utils._os import safe_join

import os
import json

from django.views.decorators.http import etag
import hashlib
#from YXSite.YXSite.baselib.components.pages.errors import handle404
from ..components.pages.errors import handle404

# Create your views here.


#def image_placeholder_etag(request, width, height):
#    content = 'Placeholder: {0} x {1}'.format(width, height)
#    return hashlib.sha1(content.encode('utf-8')).hexdigest()


def get_page_or_404(name):
    """Return page content as a Django template or raise 404 error."""
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        return None
        #raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            return None
            #raise Http404('Page Not Found')

    with open(file_path, 'r') as f:
        page = Template(f.read())
    meta = None
    for i, node in enumerate(list(page.nodelist)):
        if isinstance(node, BlockNode) and node.name == 'context':
            meta = page.nodelist.pop(i)
            break
    page._meta = meta
    return page


def page(request, slug='index'):
    """Render the requested page if found."""
    file_name = '{}.html'.format(slug)
    the_page = get_page_or_404(file_name)
    if the_page is None:
        return handle404(request, 'Page Not Found')
    else:
        context = {
            'slug': slug,
            'page': the_page,
        }
        if the_page._meta is not None:
            meta = the_page._meta.render(Context())
            extra_context = json.loads(meta)
            context.update(extra_context)

    return render(request, 'page.html', context)


    #return HttpResponse('Hello world page !!')

    #example = reverse('placeholder', kwargs={'width': 50, 'height':50})
    #context = {
    #    'example': request.build_absolute_uri(example)
    #}
    #return render(request, 'doc.html', context)
