from django import template

import markdown

register = template.Library()

@register.filter(name='md')
def md(value):
	return markdown.markdown(value)
