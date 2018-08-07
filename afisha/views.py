import requests
from django.shortcuts import HttpResponse
from django.shortcuts import render


# вывод страницы стписка фильмов
def list(request):
    return render(request, 'index.html')
