from django.conf.urls import patterns, url
from polls import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<poll_id>\d+)/like/$', views.like, name='like'),
    url(r'^(?P<poll_id>\d+)/likes/$', views.likes, name='likes'),
    url(r'^(?P<poll_id>\d+)/popularity/$', views.popularity, name='popularity'),
    url(r'^popular$', views.MostPopularFeed(), name='popular'),
)
