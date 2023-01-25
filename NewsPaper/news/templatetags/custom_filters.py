from django import template

from .utils import curse_words


register = template.Library()

@register.filter()
def curse(string: str) -> str:
    if not isinstance(string, str):
        raise ValueError("The curse filter may only be applied to strings")
    
    result_string = string
    for curse in curse_words:
       result_string = result_string.replace(curse, curse[:1] + '*' * (len(curse) - 1))
    return result_string
