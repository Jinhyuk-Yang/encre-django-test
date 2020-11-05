from django.urls import path, include
from rest_framework.routers import DefaultRouter
from doc import views

app_name = 'doc'

router = DefaultRouter()

urlpatterns = [
    path('mine', views.MyIndicesView.as_view(), name='my_indices'),
    path('<int:doc_id>', views.DocIndexView.as_view(), name='doc'),
]