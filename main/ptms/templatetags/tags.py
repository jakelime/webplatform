from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def get_sw_version():
    return 'hahah'
    # return settings.SW_VERSION