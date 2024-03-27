from django import template
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('inclusion_tags/online_status.html')
def online_status():
    return {'online_status': cache.get('computing_server_online')}
