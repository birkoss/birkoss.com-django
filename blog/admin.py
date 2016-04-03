import django
from django.contrib import admin
from django.forms import ModelForm
from django.db import models
from django.db.models import TextField

from .models import Post, Category

from markdownx.widgets import AdminMarkdownxWidget

# Show the categories field with a parent/children ordering
class PostModelForm(ModelForm):
	# class Meta:
	# 	widgets = {
	# 		'content': AdminMarkdownxWidget(),
	# 	}
	def __init__(self, *args, **kwargs):
		super(PostModelForm, self).__init__(*args, **kwargs)
		w = self.fields['categories'].widget
		choices = []
		for category in Category.objects.all():
			choices.append((category.id, category.get_name()))

		w.choices = choices


class PostModelAdmin(admin.ModelAdmin):
	form = PostModelForm
	formfield_overrides = {
		models.TextField: {'widget': AdminMarkdownxWidget},
	}

	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)


class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ('get_name','position')
	class Meta:
		model = Category

admin.site.register(Category, CategoryModelAdmin)
