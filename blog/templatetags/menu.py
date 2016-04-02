from django import template

from blog.models import Category

register = template.Library()

@register.inclusion_tag('menu.html')
def show_menu_categories():
    links = Category.objects.all()
    return {'links': links}
