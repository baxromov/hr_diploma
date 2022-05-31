import random
from django import template

register = template.Library()

@register.simple_tag
def random_int(start, stop):
    return random.randint(start, stop)