from django import template

register = template.Library()


@register.filter
def div(value, div):
    return round((value / div *10), 2)

@register.filter
def money(value, money):
    print(value, money, 'sadfdsfdsafdsafds')
    return round((value * money ), 2)