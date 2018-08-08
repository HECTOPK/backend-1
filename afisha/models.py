from django.db import models

class Film(models.Model):
	name = models.CharField(max_length=200, null=True, default=None)
	about = models.CharField(max_length=1000, null=True, default=None)
	poster_url = models.URLField(null=True, default=None)
	movie_id = models.IntegerField(default=0)
	trailer_url = models.URLField(null=True, default=None)
	genres = models.CharField(max_length=1000, null=True, default=None)
	runtime = models.IntegerField(default=None, null=True)

class Cinema(models.Model):
	name = models.CharField(max_length=200, null=True, default=None)
	address = models.CharField(max_length=200, null=True, default=None)
	cinema_id = models.IntegerField(default=0)

class Seance(models.Model):
	film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='seances')
	cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='seances')
	time = models.TimeField(null=True, default=None)
	date = models.DateField(null=True, default=None)
