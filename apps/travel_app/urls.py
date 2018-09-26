from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^my_trips$', views.my_trips),
    url(r'^saved_itineraries$', views.saved_itineraries),
    url(r'^edit_trip/(?P<t_id>\d+)$', views.edit_trip),
    url(r'^edit_process$', views.edit_process),
    url(r'^add_process$', views.add_process),
    url(r'^login_reg$', views.login_reg),
    url(r'^login_process$', views.login_process),
    url(r'^register_process$', views.register_process),
    url(r'^logout$', views.logout),
    url(r'^view/(?P<t_id>\d+)$', views.view_trip),
    url(r'^delete/(?P<t_id>\d+)$', views.delete),
    url(r'^remove/(?P<t_id>\d+)$', views.remove),
    url(r'^find_places$', views.find_places),
    url(r'^save/(?P<t_id>\d+)$', views.save_process),
    url(r'^results/(?P<city>\w+)/(?P<country>\w+)$', views.results),
]