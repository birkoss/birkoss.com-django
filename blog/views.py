from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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

	print(kwargs)

	instance = get_object_or_404(Category, *args, **kwargs)

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
		'title': instance.name,
		'objects': queryset,
	}

	return render(request, 'blog/posts.html', context)
