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


	header_title = instance.name
	header_icon = instance.icon
	if instance.parent:
		header_icon = instance.parent.icon
		header_title = "%s / %s" % (instance.parent.name, header_title)

	context = {
		'header_title': header_title,
		'header_icon': header_icon,
		'category': instance,
		'objects': queryset,
		'empty_content': 'Aucun article dans cette catégorie',
	}

	return render(request, 'blog/posts.html', context)


def search(request):

	query = request.GET.get("q")
	if query:
		queryset = Post.objects.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query)
		).distinct()

	context = {
		'header_title': 'Recherche pour %s' % (query),
		'header_icon': 'search',
		'objects': queryset,
		'empty_content': 'Aucun article trouvé avec cette recherche',
	}

	return render(request, 'blog/posts.html', context)


def post_detail(request, *args, **kwargs):

	instance = get_object_or_404(Post, *args, **kwargs)

	context = {
		'post': instance,
	}

	return render(request, 'blog/post.html', context)
