from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from .models import Test
from .serializers import TestSerializer


def index(request):
    return HttpResponse("Lorem Ipsum")


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class UserSignUp(views.APIView):
    def post(self, request):
        username = request.data['name']
        password = request.data['password']
        email = request.data['email']
        try:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    username=username, password=password, email=email)
                user = authenticate(username=username, password=password)
                login(request, user)
                return Response("Sign up successful")
            else:
                return Response("User already exists")
        except Exception as e:
            return Response("Sign up failed. "+str(e))
