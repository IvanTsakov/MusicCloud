from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def highlight(text, word):
	return mark_safe(text.lower().replace(word.lower(),"<span class='highlight'>%s</span>" % word))


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value