from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    token = Token.objects.create(user=user)
                    return Response({"status": "Sign up successful", "token": token.key})
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
        user = authenticate(username=username, password=password)
        if user is not None:
            token = Token.objects.create(user=user)
            return Response({"status": "Login successful", "token": token.key})

        else:
            return Response("Username or password incorrect")


class UserLogout(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Token.objects.get(user=request.user).delete()
        return Response("Logout successful")


class GetCredits(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        credits = UserData.objects.get(id=request.user)
        res = serializers.serialize("json", [credits])
        return Response(res)


class UploadForPrinting(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        path = request['files'].file.path
        from_page = request['from']
        to_page = request['to']
        credits = from_page - to_page
        color = request['color']

        if remove_credits(request.user, credits, False):
            print_file(path, from_page, to_page, color)
            remove_credits(request.user, credits, True)
            return Response("Document printed successfully. " + credits + " credits used up")
        return Response("You do not have enough credits")


def remove_credits(user, credits_to_remove, printing_complete):
    data = UserData.objects.get(id=user)
    if data.credits - credits_to_remove >= 0:
        if printing_complete:
            data.credits -= credits_to_remove
            data.save()
        return True
    return False


def print_file(path, from_page, to_page, color):
    # SEND FILE TO PRINTER FOR PRINTING
    pass
