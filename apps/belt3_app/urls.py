from django.conf.urls import url
from . import views
from django.core.urlresolvers import reverse

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^posts$', views.posts),    
    url(r'^users/(?P<id>\d+)$', views.show), 
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^removefav/(?P<id>\d+)$', views.removefav),    
    url(r'^logout', views.logout),
    url(r'^log', views.log),

]