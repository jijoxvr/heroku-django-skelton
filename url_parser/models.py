import hashlib
import unicodedata
from django.conf import settings

from django.db.models import F
from django.db import models


class UrlManager(models.Manager):

    @staticmethod
    def hash_function(input_url):
        inp = unicodedata.normalize('NFKD', input_url).encode('ascii', 'ignore')
        return settings.SHORT_URL_ENDPOINT + hashlib.md5(inp).hexdigest()[:8]

    def insert_or_fetch_url(self, long_url):
        url_obj = self.filter(long_url=long_url).first()
        if not url_obj:
            url_obj = URLMapper(long_url=long_url, short_url=str(self.hash_function(long_url)))
            url_obj.save()
        return url_obj

    def get_url_from_short(self, short_url):
        return self.filter(short_url=short_url).first()

    def increment_fetch_count(self, short_url):
        self.filter(short_url=short_url).update(fetch_count=F('fetch_count') + 1)


# Create your models here.
class URLMapper(models.Model):
    long_url = models.TextField(primary_key=True)
    short_url = models.CharField(max_length=50)
    fetch_count = models.IntegerField(default=0)
    objects = UrlManager()



