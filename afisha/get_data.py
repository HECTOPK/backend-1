import datetime, time
from .models import *
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests, re

def get_data_from_kp(day, month, year):
	import requests
	from bs4 import BeautifulSoup
	page_url = 'https://www.kinopoisk.ru/afisha/city/461/day_view/' + str(year) + '-' + str(month) + '-' + str(day) + '/'
	page = requests.get(page_url)
	page = page.content
	soup = BeautifulSoup(page, "html.parser")
	films = soup.findAll('div', attrs={'class': 'films_metro'})
	print(len(films))
	for film in films:
		soup = BeautifulSoup(str(film), "html.parser")
		title = soup.find('div', attrs={'class': 'title'})
		about = BeautifulSoup(str(title), "html.parser").find('ul', {'class': 'film_info'})
		title = BeautifulSoup(str(title), "html.parser").find('a')
		try:
			film_object = Film.objects.get(name=title.get_text())
		except Film.DoesNotExist:
			film_object = Film()
			film_object.name = title.get_text()
			film_object.about = re.sub("<.*?>",' ', str(about.get_text()))
			film_object.url = title['href']
			film_object.save()
		cinemas = soup.findAll('dl', attrs={'class': 'cinema_row'})
		for cinema in cinemas:
			soup = BeautifulSoup(str(cinema), "html.parser")
			name = soup.find('dt', attrs={'class': 'name'})
			name = BeautifulSoup(str(name), "html.parser").find('a')
			try:
				cinema_object = Cinema.objects.get(url=name['href'])
			except Cinema.DoesNotExist:
				cinema_object = Cinema()
				cinema_object.name = name.get_text()
				cinema_object.url = name['href']
				cinema_object.save()
			times = soup.findAll('dd', attrs={'class': 'time'})
			for string_of_time in times:
				soup = BeautifulSoup(str(string_of_time), "html.parser")
				for time in soup.findAll('i'):
					seance_object = Seance()
					seance_object.film = film_object
				for time in soup.findAll('b'):
					seance_object = Seance()
					seance_object.film = film_object
					seance_object.cinema = cinema_object
					seance_object.date = datetime.date(day=day, month=month, year=year)
					seance_object.time = datetime.datetime.strptime(BeautifulSoup(str(time), "html.parser").find('a').get_text(), '%H:%M').time()
					seance_object.save()
					print(seance_object.film.name + '  ' + str(seance_object.date) + '  ' + str(seance_object.time))

def get_data(request):
	for i in range(0,7):
		if Seance.objects.filter(date=datetime.date.today() + datetime.timedelta(days=i)).count() > 0:
			continue
		day = (datetime.date.today() + datetime.timedelta(days=i)).day
		month = (datetime.date.today() + datetime.timedelta(days=i)).month
		year = (datetime.date.today() + datetime.timedelta(days=i)).year
		get_data_from_kp(day, month, year)
	return HttpResponse('data saved')


def del_data(request):
	for item in Cinema.objects.all():
		item.delete()
	for item in Film.objects.all():
		item.delete()
	for item in Seance.objects.all():
		item.delete()
	return HttpResponse('deleted')
