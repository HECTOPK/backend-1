from django.urls import path
from afisha import views

urlpatterns = [
    path('', views.list),
]