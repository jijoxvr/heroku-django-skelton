from django.urls import include, path, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('url_parser.urls')),
]
