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
    path('shop/',views.Shop.as_view(), name='shop'),
    path('cart/',views.Cart.as_view(), name='cart'),
    path('login/',views.login.as_view(), name='login'),
    path('signup/',views.signup,name = 'signup'),
    path('checkout/',views.Checkout.as_view(), name='checkout'),
    path('order/',views.Order.as_view(), name='order'),
]