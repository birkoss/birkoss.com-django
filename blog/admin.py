from django.contrib import admin
from django.forms import ModelForm
from django.db.models import TextField

from .models import Post, Category


# Show the categories field with a parent/children ordering
class PostModelForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostModelForm, self).__init__(*args, **kwargs)
		parents = Category.objects.filter(parent=None)
		w = self.fields['categories'].widget
		choices = []
		for choice in parents:
			choices.append((choice.id, choice.name))
			for child in Category.objects.filter(parent=choice.id):
				choices.append((child.id, child.get_name()))

		w.choices = choices


class PostModelAdmin(admin.ModelAdmin):
	form = PostModelForm
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)


# Show the parent field with a parent/children ordering
class CategoryModelForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(CategoryModelForm, self).__init__(*args, **kwargs)
		parents = Category.objects.filter(parent=None)
		w = self.fields['parent'].widget
		choices = []
		for choice in parents:
			choices.append((choice.id, choice.name))
			for child in Category.objects.filter(parent=choice.id):
				choices.append((child.id, child.get_name()))

		w.choices = choices


class CategoryModelAdmin(admin.ModelAdmin):
	form = CategoryModelForm
	class Meta:
		model = Category

admin.site.register(Category, CategoryModelAdmin)
