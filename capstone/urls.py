from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name = 'home'),
    path('home/',views.home,name = 'home'),
    path('about/',views.about,name = 'about'),
    path('service/',views.service,name = 'service'),
    path('recent/',views.recent,name = 'recent'),
    path('conatcts/',views.contacts,name = 'contacts'),
    path('shop/',views.shop, name='shop'),
    path('cart/',views.Cart, name='cart'),
    path('login/',views.login,name = 'login'),
    path('signup/',views.signup,name = 'signup'),
]