from django import template
from django.shortcuts import render
from django.template import Template
from django.template import loader
from django.template import Context

import threading

register = template.Library()


class CardTemplate(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.template = loader.get_template('card.html')

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(CardTemplate, "_instance"):
            with CardTemplate._instance_lock:
                if not hasattr(CardTemplate, "_instance"):
                    CardTemplate._instance = CardTemplate(*args, **kwargs)
        return CardTemplate._instance


class IndexCard(template.Node):

    def __init__(self, listname):
        self.listname = listname

    def render(self, context):
        card_data = context.get(self.listname)
        t = CardTemplate.instance().template
        return t.render(card_data)


def index_card(parser, token):

    try:
        tagname, listname = token.split_contents()
        return IndexCard(listname)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag(index_card) argument error:" % token.contents.split()[0])

    # return IndexCard()


register.tag('index_card', index_card)

