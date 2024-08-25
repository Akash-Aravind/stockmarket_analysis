from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('currentprice/<str:ticker>/', views.currentprice, name='currentprice'),
    path('pricehistory/<str:ticker>/', views.pricehistory, name='pricehistory'),
]