from django import template

register = template.Library()


@register.filter(name='inc')
def inc(value, arg):
    return int(value) + int(arg)


@register.simple_tag
def division(a, b, **args):
    a, b = int(a), int(b)
    if "to_int" in args:
        return int(a / b)
    else:
        return a / b
