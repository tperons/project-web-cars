import re

from django import template

register = template.Library()


@register.filter
def phone_format(value):
    if value:
        digits = re.sub(r'\D', '', str(value))

        if len(digits) == 13:
            return f'+{digits[0:2]} ({digits[2:4]}) {digits[4:5]} {digits[5:9]} {digits[9:13]}'
        return value
    return ''
