from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):

    cardlist = []
    for i in range(10):
        img = {
            'title': 'img Title',
            'url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1549389489258&di=83bb99a49665a523d8f1d5423d8f08a0&imgtype=0&src=http%3A%2F%2Fx1.cncnimg.cn%2Fp10057%2F143%2F5de8.png',
            'alt': 'Card image cap %d' % i,
        }
        buttons = [
            {'title': '打开', 'url': 'http://www.baidu.com'},
            {'title': '管理', 'url': 'www.google.com'}
        ]
        card = {
            'desc': 'text_string',
            'img': img,
            'flag': 'flag_%d' % i,
            'buttons': buttons
        }
        cardlist.append(card)
    return render(request, 'index2.html', context={'cards': cardlist})
    # return HttpResponse("index page")
