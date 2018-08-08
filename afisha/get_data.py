import datetime, time, json
from .models import *
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests, re
import dateutil.parser
import iso8601

def del_data(request):
	for item in Cinema.objects.all():
		item.delete()
	for item in Film.objects.all():
		item.delete()
	for item in Seance.objects.all():
		item.delete()
	return HttpResponse('deleted')

def get_data(request):
	try:
		response = requests.get(url="https://api.internationalshowtimes.com/v4/showtimes", params={'countries': 'GB', 'fields': 'id,movie_id,cinema_id,start_at','location':'51.51,-0.13', 'distance': '500'}, headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'},)
		data = response.json()['showtimes']
		#return HttpResponse(response.content)
		i = 1
		for item in data:
			if item['cinema_id'] == None or item['movie_id'] == None:
				continue
			print(str(i) + ') ' + item['cinema_id'] + '  ' + item['movie_id'])
			try:
				film_object = Film.objects.get(movie_id=item['movie_id'])
			except Film.DoesNotExist:
				film_response = requests.get(url="https://api.internationalshowtimes.com/v4/movies/" + str(item['movie_id']), params={}, headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'},)
				film_data = film_response.json()
				film_object = Film()
				try:
					film_object.movie_id = item['movie_id']
					film_object.name = film_data['movie']['original_title']
					film_object.about = film_data['movie']['synopsis']
					film_object.poster_url = film_data['movie']['poster_image']['image_files'][6]['url']
					film_object.trailer_url = film_data['movie']['trailers'][0]['trailer_files'][0]['url']
					film_object.trailer_url = str.replace(film_object.trailer_url, 'watch?v=','embed/')
					film_object.runtime = int(film_data['movie']['runtime'])
					film_object.genres = json.dumps(film_data['movie']['genres'])
					film_object.genres = float(film_data['raitings']['imdb']['value'])
					print(str(film_data['movie']['genres']))
				except TypeError:
					print('TypeError')

				film_object.save()
			try:
				cinema_object = Cinema.objects.get(cinema_id=item['cinema_id'])
			except Cinema.DoesNotExist:
				cinema_responce = requests.get(url="https://api.internationalshowtimes.com/v4/cinemas/" + item['cinema_id'], headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'},)
				cinema_data = cinema_responce.json()
				cinema_object = Cinema()
				cinema_object.cinema_id = item['cinema_id']
				cinema_object.name = cinema_data['cinema']['name']
				cinema_object.address = cinema_data['cinema']['location']['address']['display_text']
				cinema_object.city = cinema_data['cinema']['location']['address']['city']
				cinema_object.save()
			seance_object = Seance()
			seance_object.film = film_object
			seance_object.cinema = cinema_object
			date = iso8601.parse_date(item['start_at'])
			seance_object.date = date.date()
			seance_object.time = date.time()
			seance_object.save()
			i += 1
		return HttpResponse(response.content)
	except requests.exceptions.RequestException:
		return HttpResponse('request error')
