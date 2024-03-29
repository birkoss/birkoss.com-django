from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^markdownx/', include('markdownx.urls')),
	url(r'^', include('blog.urls', namespace='blog')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
