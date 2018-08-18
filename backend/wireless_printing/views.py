from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from .models import Test, UserData
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
            if not request.user.is_authenticated:
                if not User.objects.filter(email=email).exists():
                    User.objects.create_user(
                        username=username, password=password, email=email)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return Response("Sign up successful")
                else:
                    return Response("User already exists")
            else:
                return Response("You are already logged in")
        except Exception as e:
            return Response("Sign up failed. "+str(e))


class UserLogin(views.APIView):
    def post(self, request):
        username = request.data['name']
        password = request.data['password']
        try:
            if not request.user.is_authenticated:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return Response("Login successful")
                else:
                    return Response("User does not exist")
            else:
                return Response("You are already logged in")
        except Exception as e:
            return Response("Sign up failed. "+str(e))


class UserLogout(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response("Logout successful")
        else:
            return Response("You must log in to log out")


class GetCredits(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            credits = UserData.objects.get(id=request.user)
            res = serializers.serialize("json", [credits])
            return Response(res)
