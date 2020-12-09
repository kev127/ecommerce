from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('home/',views.home,name = 'home'),
    url('about/',views.about,name = 'about'),
    url('service/',views.service,name = 'service'),
    url('recent/',views.recent,name = 'recent'),
]