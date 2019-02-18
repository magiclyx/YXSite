from django.shortcuts import render

# Create your views here.


def openiconic(request):
    return render(request, 'openiconic.html')


def glyphicon(request):
    return render(request, 'glyphicon.html')