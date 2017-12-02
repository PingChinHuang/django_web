from django import template

register = template.Library()

@register.filter(name = 'remainder')
def remainder(value, arg):
	print(value)
	print(arg)
	return value % arg

