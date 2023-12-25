from django import template
import re

register = template.Library()

@register.filter(name='split_last')
def split_last(value):
    if value:
        path = str(value)
        name = re.split(r"\d+[\.,]?\d*", path)[-2]
        print(f"\n\n{name}\n\n")
        result = re.sub(r'[^\u0400-\u04FF\s]+', '', name)
    else:
        result = 'Парфюмерная вода'

    return result

# @register.filter(name="check_name")
# def title_changer(value):
#     if len(str(value)) > 24:
#         return f'<h3 class="card__title" style="font-size: 15px;">{{ value|check_name  }}</h3>'
#     else:
#         return value