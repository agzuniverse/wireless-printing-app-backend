from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from .models import Test
from .serializers import TestSerializer


def index(request):
    return HttpResponse("Lorem Ipsum")


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
