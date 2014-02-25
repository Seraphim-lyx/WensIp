from django import template

register = template.Library()

@register.filter
def remainder(value):
    if int(value)%2 is 0:
        return "#E5E5E5"
