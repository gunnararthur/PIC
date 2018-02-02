from django import template

register = template.Library()

# @register.filter
# def get_at_index(listi, index):
#     try:
#         val = listi[index]
#     except IndexError:
#         val = ''
#     if val == 'x':
#         return ''
#     else: return val

@register.simple_tag
def get_at_index(student, round_nr, index):
    if int(round_nr) is 1:
        listi = student.ans1
    elif int(round_nr) is 2:
        listi = student.ans2
    elif int(round_nr) is 3:
        listi = student.ans3
    try:
        val = listi[index]
    except IndexError:
        val = ''
    if val == 'x':
        return ''
    else: return val

@register.simple_tag
def get_val_at_index(l, index):
    return l[index]
