from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity


# All of this is straight from the django documentation by the way
# so if you'd like a deeper explanation of how it works
# just go there and look up creating custom template tags and filters.