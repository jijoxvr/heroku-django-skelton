from django.conf import settings

from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import ShortURlRequest, LongURlRequest, is_short_url_valid
from .models import URLMapper
import validators


class UrlParser(viewsets.ViewSet):

    model = URLMapper

    def fetch_short_url(self, request):
        serialized_data = ShortURlRequest(data=request.data)

        if serialized_data.is_valid():
            long_url = serialized_data.validated_data.get('long_url')
            url_obj = self.model.objects.insert_or_fetch_url(long_url=long_url)
            return Response({
                "short_url": url_obj.short_url,
                "status": "OK",
                "status_codes": []
            }, status=status.HTTP_200_OK)

        # HTTP_400_BAD_REQUEST status is more suitable
        return Response({
            "status": "FAILED",
            "status_codes": ["INVALID_URLS"]
        }, status=status.HTTP_200_OK)

    def fetch_long_url(self, request):
        serialized_data = LongURlRequest(data=request.data)

        if serialized_data.is_valid():
            short_url = serialized_data.validated_data.get('short_url')
            url_obj = self.model.objects.get_url_from_short(short_url=short_url)
            if url_obj:
                return Response({
                    "long_url": url_obj.long_url,
                    "status": "OK",
                    "status_codes": []
                }, status=status.HTTP_200_OK)
        return Response({
            "status": "FAILED",
            "status_codes": ["SHORT_URLS_NOT_FOUND"]
        }, status=status.HTTP_200_OK)

    def fetch_multiple_short_url(self, request):
        long_urls = request.data.get('long_urls')
        invalid_urls = []
        if long_urls:
            for ur in long_urls:
                if not validators.url(ur):
                    invalid_urls.append(ur)
        if len(invalid_urls) > 0:
            return Response({
                "invalid_urls": invalid_urls,
                "status": "FAILED",
                "status_codes": ["INVALID_URLS"]
            }, status=status.HTTP_200_OK)
        response_data = {}
        if long_urls:
            for ur in long_urls:
                response_data[ur] = self.model.objects.insert_or_fetch_url(long_url=ur).short_url

        return Response({
            "short_urls": response_data,
            "invalid_urls": [],
            "status": "OK",
            "status_codes": []
        }, status=status.HTTP_200_OK)

    def fetch_multiple_long_urls(self, request):
        short_urls = request.data.get('short_urls')
        invalid_urls = []
        if short_urls:
            for ur in short_urls:
                if not is_short_url_valid(ur):
                    invalid_urls.append(ur)
        if len(invalid_urls) > 0 or not short_urls:
            return Response({
                "invalid_urls": invalid_urls,
                "status": "FAILED",
                "status_codes": ["SHORT_URLS_NOT_FOUND"]
            }, status=status.HTTP_200_OK)
        response_data = {}
        for ur in short_urls:
            url_obj = self.model.objects.get_url_from_short(short_url=ur)
            if url_obj:
                response_data[ur] = url_obj.long_url

        return Response({
            "long_urls": response_data,
            "invalid_urls": [],
            "status": "OK",
            "status_codes": []
        }, status=status.HTTP_200_OK)

    def redirect_to_actual_url(self, request, *args, **kwargs):
        short_url_hash = kwargs.get('short_url_hash')
        if short_url_hash:
            short_url = settings.SHORT_URL_ENDPOINT + short_url_hash
            self.model.objects.increment_fetch_count(short_url=short_url)
        return Response({}, status=status.HTTP_302_FOUND)

    def get_fetch_count(self, request):
        serialized_data = LongURlRequest(data=request.data)
        if serialized_data.is_valid():
            short_url = serialized_data.validated_data.get('short_url')
            url_obj = self.model.objects.get_url_from_short(short_url=short_url)
            if url_obj:
                return Response({
                    "count": url_obj.fetch_count,
                    "status": "OK",
                    "status_codes": []
                }, status=status.HTTP_200_OK)
        return Response({
            "status": "FAILED",
            "status_codes": []
        }, status=status.HTTP_200_OK)

    def clear_db(self, request):
        self.model.objects.all().delete()
        return Response({}, status=status.HTTP_200_OK)


