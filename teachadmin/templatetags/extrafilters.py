from django import template

register = template.Library()

@register.filter
def get_type(value):
    """ Checks if the passed variable 'value' is of type 'arg'
        INPUT: Value - Python core-type (int, float, dict etc.) variable
        OUTPUT: Bool (True/False)"""

    return type(value)

# register.filter('isinst', isinst)
