from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from user import views

urlpatterns = [
    url(r'^signup', views.UserRegistrationView.as_view()),
    url(r'^login', views.UserLoginView.as_view()),
]