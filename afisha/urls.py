from django.urls import path
from django.conf.urls import url
from afisha import views, get_data

urlpatterns = [
	url(r'get_data', get_data.get_data),
	url(r'del_data', get_data.del_data),
	path('', views.list),

]
