from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^categorie/(?P<slug>[\w-]+)/$', views.category, name='category'),
	url(r'^categorie/(?P<parent__slug>[\w-]+)/(?P<slug>[\w-]+)/$', views.category, name='subcategory'),
]
