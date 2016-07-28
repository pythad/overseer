from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$', views.DistributorGroupDetailView.as_view(),
        name='distributor'),
    url(r'^(?P<pk>[\d]+)/edit/$',
        views.DistributorGroupUpdateView.as_view(), name='edit_distributor'),
    url(r'^update/$',
        views.update_distributor, name='update_distributor'),
    url(r'^favorite/$',
        views.favorite_distributor, name='favorite_distributor'),
]
