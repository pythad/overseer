from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^queries/$', views.QueryListView.as_view(),
        name='queries'),
    url(r'^queries/(?P<pk>[\d]+)$', views.QueryDetailView.as_view(),
        name='query'),
    url(r'^queries/create_query$', views.QueryCreateView.as_view(),
        name='add_query'),
    url(r'^queries/(?P<pk>[\d]+)/delete/$',
        views.QueryDeleteView.as_view(), name='delete_query'),
    url(r'^sections/$', views.SectionListView.as_view(), name='sections'),
    url(r'^sections/(?P<pk>[\d]+)$', views.SectionDetailView.as_view(),
        name='section'),
    url(r'^sections/create_section$',
        views.SectionCreateView.as_view(), name='add_section'),
    url(r'^sections/(?P<pk>[\d]+)/delete/$',
        views.SectionDeleteView.as_view(), name='delete_section'),
    url(r'^distributors/$', views.DistributorListView.as_view(),
        name='distributors'),
    url(r'^distributors/person/', include('people.urls', namespace='people')),
    url(r'^distributors/group/', include('groups.urls', namespace='groups')),
    url(r'^distributors/my_favorite_distributors$',
        views.my_favorite_distributors, name='my_favorite_distributors'),
    url(r'^distributors/all_distributors$',
        views.all_distributors, name='all_distributors'),
    url(r'^distributors/by_mentions_distributors$',
        views.by_mentions_distributors, name='by_mentions_distributors'),
    url(r'^distributors/search_dist', views.search_dist, name='search_dist'),
]
