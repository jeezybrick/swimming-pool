
from django.conf.urls import url
from django.views.generic import TemplateView
from my_auth import views


urlpatterns = [

    # Auth views
    url(r'^login/$', views.LoginView.as_view(),
        name='login'),
    url(r'^auth/logout/$', views.get_logout, name='logout'),

]
