from django.db import models

class Film(models.Model):
	name = models.CharField(max_length=200, null=True, default=None)
	about = models.CharField(max_length=1000, null=True, default=None)
	url = models.URLField(null=True, default=None)

class Cinema(models.Model):
	name = models.CharField(max_length=200, null=True, default=None)
	url = models.URLField(null=True, default=None)

class Seance(models.Model):
	film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='seances')
	cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='seances')
	time = models.TimeField()
	date = models.DateField()
