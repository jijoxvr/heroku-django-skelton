from django.urls import path, re_path
from .views import UrlParser

urlpatterns = [
    path(r'fetch/short-url/', UrlParser.as_view({'post': 'fetch_short_url'}), name="short_url"),
    path(r'fetch/short-urls/', UrlParser.as_view({'post': 'fetch_multiple_short_url'}), name="short_urls"),
    path(r'fetch/long-url/', UrlParser.as_view({'post': 'fetch_long_url'}), name="long_url"),
    path(r'fetch/long-urls/', UrlParser.as_view({'post': 'fetch_multiple_long_urls'}), name="long_urls"),
    path(r'fetch/count/', UrlParser.as_view({'post': 'get_fetch_count'}), name="fetch_count"),
    path(r'clean-urls/', UrlParser.as_view({'post': 'clear_db'}), name="clean_database"),
    re_path(r'(?P<short_url_hash>[a-zA-Z0-9_]{0,8})', UrlParser.as_view({'post': 'redirect_to_actual_url'}),
            name="redirect"),

]
