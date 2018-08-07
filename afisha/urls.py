from django.urls import path
from django.conf.urls import url
from afisha import views, get_data


urlpatterns = [
	url(r'^get_data$', get_data.get_data),
	url(r'^del_data$', get_data.del_data),
	url(r'^film/(?P<film_id>\d+)$', views.film_page, name='film_url'),
	url(r'^film/(?P<film_id>\d+)/(?P<date>\d+\-\d+\-\d+)$', views.film_page_with_date, name='film_with_date_url'),
	url(r'^$', views.list_page, name='home_url'),
]
