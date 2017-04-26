from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'', views.index),
    url(r'^about/$',  views.about, name='about'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
