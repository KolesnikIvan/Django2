from django import template
# from django.conf import settings

register = template.Library()

@register.simple_tag
def sample_template_tag(string):
    return f'sample {string}'
    
@register.filter(name='other_sample')
def sample_template_filter(string):
    return f'other sample {string}'
    