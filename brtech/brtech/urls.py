from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^cities/(?P<slug>[A-Za-z_\-\(\)\/]+)/?$', 'main.views.cities', name='main_views_cities'),
    url(r'^airports/info/(?P<slug>[A-Za-z_\-\(\)\/]+)/?$', 'main.views.airports_info', name='main_views_airports_info'),
    url(r'^airports/(?P<slug>[A-Za-z_\-\(\)\/]+)/?$', 'main.views.airports', name='main_views_airports'),

)
