from django.conf.urls import url

from .views import index, home, signup

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^home$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
]
