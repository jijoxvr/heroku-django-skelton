from rest_framework import serializers
from django.conf import settings


class ShortURlRequest(serializers.Serializer):
    long_url = serializers.URLField(required=True)


class MultipleShortURlRequest(serializers.Serializer):
    long_urls = serializers.ListField(serializers.URLField)


class LongURlRequest(serializers.Serializer):
    short_url = serializers.CharField(required=True)

    def validate_short_url(self, value):
        if not is_short_url_valid(value):
            raise serializers.ValidationError("Invalid short url")
        return value


def is_short_url_valid(value):
    if not value.startswith(settings.SHORT_URL_ENDPOINT):
        return False
    if len(value.split('/')[1]) > 8:
        return False
    return True
