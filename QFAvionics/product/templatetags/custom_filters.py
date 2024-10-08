from django import template

register = template.Library()

@register.filter
def card_size(num_categories):
    return 12 // num_categories
