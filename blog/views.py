from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Post

def home(request):
	queryset_list = Post.objects.all()

	paginator = Paginator(queryset_list, 25)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'objects': queryset,
	}

	return render(request, 'blog/posts.html', context)

def category(request, *args, **kwargs):

	instance = get_object_or_404(Category, *args, **kwargs)

	queryset_list = Post.objects.filter( Q(categories__id=instance.id) | Q(categories__parent__id=instance.id) ).distinct()

	paginator = Paginator(queryset_list, 25)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'category': instance,
		'objects': queryset,
	}

	return render(request, 'blog/posts.html', context)


def post_detail(request, *args, **kwargs):

	instance = get_object_or_404(Post, *args, **kwargs)

	queryset_list = Post.objects.filter(categories__id=instance.id)

	paginator = Paginator(queryset_list, 25)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'category': instance,
		'objects': queryset,
	}

	return render(request, 'blog/posts.html', context)
