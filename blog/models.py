from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.CharField(max_length=100, blank=True)
	position = models.IntegerField(blank=True, editable=False)

	parent = models.ForeignKey('self', blank=True, null=True, related_name="children")

	class Meta:
		ordering = ('position',)
		verbose_name_plural = "Categories"
		verbose_name = "Categorie"

	def __str__(self):
		return self.name
		# return ("-- " if self.parent != None else "") + self.name

	def get_name(self):
		return ("-- " if self.parent != None else "") + self.name
	get_name.short_description = 'Name'

	def generate_slug(self, new_slug=None):
		qs = Category.objects.filter(slug=new_slug).order_by('-id')
		exists = qs.exists()
		if exists:
			new_slug = "%s-%s" % (new_slug, qs.first().id)
			return self.generate_slug(new_slug=new_slug)
		return new_slug

	def get_absolute_url(self):
		if self.parent is None:
			return reverse('blog:category', kwargs={'slug': self.slug})
		return reverse('blog:subcategory', kwargs={'slug': self.slug, 'parent__slug': self.parent.slug})

	@staticmethod
	def pre_save(sender, instance, *args, **kwargs):
		order = 1
		parents = Category.objects.filter(parent=None)
		for parent in parents:
			Category.objects.filter(pk=parent.pk).update(position=order)
			order += 1
			children = Category.objects.filter(parent=parent.id).order_by('name',)
			for child in children:
				Category.objects.filter(pk=child.pk).update(position=order)
				order += 1

		if not instance.slug:
			instance.slug = instance.generate_slug(new_slug=slugify(instance.name))

pre_save.connect(Category.pre_save, Category)


class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	slug = models.SlugField(max_length=100, blank=True)

	date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	date_published = models.DateField(auto_now_add=True, auto_now=False)

	categories = models.ManyToManyField(Category)
	# tags = models.ManyToMany(tag)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('-date_published', '-date_created', '-date_modified')

	def generate_slug(self, new_slug=None):
		qs = Post.objects.filter(slug=new_slug).order_by('-id')
		exists = qs.exists()
		if exists:
			new_slug = "%s-%s" % (new_slug, qs.first().id)
			return self.generate_slug(new_slug=new_slug)
		return new_slug

	@staticmethod
	def pre_save(sender, instance, *args, **kwargs):
		# @TODO Select parents categories on save
		if not instance.slug:
			instance.slug = instance.generate_slug(new_slug=slugify(instance.title))

pre_save.connect(Post.pre_save, Post)
