
from django.conf.urls import url
from django.views.generic import TemplateView
from my_auth import views


urlpatterns = [

    url(r'^auth/logout/$', views.get_logout, name='logout'),

]
