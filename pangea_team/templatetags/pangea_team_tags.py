from django import template

register = template.Library()

@register.simple_tag
def get_val_at_index(l, index):
    return list[index]
