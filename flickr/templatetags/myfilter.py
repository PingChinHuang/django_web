from django import template

register = template.Library()

@register.filter(name = 'remainder')
def remainder(value, arg):
	print(value)
	print(arg)
	return value % arg

@register.filter(name = 'div')
def div(value, arg):
	print(value)
	print(arg)
	return int(value) / arg

@register.filter(name = 'range')
def _range(value):
	return range(value)
