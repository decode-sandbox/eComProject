from django import template

register = template.Library()

@register.filter
def item(dict_,idx):   
    return dict_[str(idx)]