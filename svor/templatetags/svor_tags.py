from django import template

register = template.Library()

@register.filter
def get_at_index(listi, index):
    try:
        val = listi[index]
    except IndexError:
        val = ''

    if val == 'x':
        return ''
    else: return val
