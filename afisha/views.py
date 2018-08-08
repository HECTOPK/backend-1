import requests, re, json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *


# вывод страницы стписка фильмов
def list_page(request):
	return render(request, 'index.html', {'all': Film.objects.all()})



def film_page_with_date(request, film_id, date):
	date = datetime.datetime.strptime(date, '%Y-%m-%d')
	context = {}
	try:
		film = Film.objects.get(id=film_id)
	except Film.DoesNotExist:
		context['error'] = 'film not found'
		return render(request, 'film_page.html', context)
		#return HttpResponseRedirect(reverse('home_url'))
	context['cinemas'] = []
	for cinema in Cinema.objects.all():
		array = []
		for item in Seance.objects.filter(cinema=cinema, date=date, film=film).order_by('time'):
			array.append(item)
		if len(array) != 0:
			context['cinemas'].append({'cinema':cinema, 'seances': array})
		#context['cinemas'].append(array)
	genres =[]
	film.genres = str.replace(film.genres,"\'", "\"")
	for item in json.loads(film.genres):
		genres.append(item['name'])
	context['genres'] = genres
	context['imdb_rating'] = film.imdb_rating
	context['runtime'] = film.runtime
	context['date'] = date
	context['film'] = film
	context['dates'] = []
	for i in range(0,7):
		if film.seances.filter(date=(datetime.date.today() + datetime.timedelta(days=i))).count() > 0:
			context['dates'].append(datetime.date.today() + datetime.timedelta(days=i))
	context['seances'] = Seance.objects.filter(film=film, date=date)

	return render(request, 'film_page.html', context)

def film_page(request, film_id):
	return film_page_with_date(request, film_id, str(datetime.date.today()))
