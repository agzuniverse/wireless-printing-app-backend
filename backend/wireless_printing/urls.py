from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('test', views.TestView)

urlpatterns = [
    path('index/', views.index, name='index'),
    path('signup/', views.UserSignUp.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view()),
    path('', include(router.urls))
]
