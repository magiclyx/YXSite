from django.shortcuts import render

# Create your views here.


def handle404(request, *args, **kwargs):
    # return HttpResponse("index page")
    title = 'Page Not Found'
    header = 'Page Not Found'
    description = 'Sorry, but the page you were trying to view does not exist.'
    return render(request, 'yxbaseError.html', context=locals(), status=404)


def handle500(request, *args, **kwargs):
    title = 'Internal Server Error'
    header = 'Internal Server Error'
    description = 'We are very sorry, It seems there is a problem with our servers.'
    return render(request, 'yxbaseError.html', context=locals(), status=500)
