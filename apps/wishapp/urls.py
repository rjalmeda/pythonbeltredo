from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^addwish$', views.addwish),
    url(r'^deletewish$', views.deletewish),
    url(r'^wishitem/(?P<itemid>\w*)$', views.wishitem),
    url(r'^create$', views.create),
    url(r'^createitem$', views.createitem),
    url(r'^deleteitem$', views.deleteitem),
    url(r'^allwishes$', views.allwishes),
    url(r'^allitems$', views.allitems)
]