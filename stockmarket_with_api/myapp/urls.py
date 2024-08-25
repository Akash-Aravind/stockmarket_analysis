from django.urls import path
from .views import TopCompaniesAPIView, CurrentPriceAPIView, PriceHistoryAPIView

urlpatterns = [
    path('api/companies/', TopCompaniesAPIView.as_view(), name='top_companies'),
    path('api/price/<str:ticker>/', CurrentPriceAPIView.as_view(), name='current_price'),
    path('api/price-history/<str:ticker>/', PriceHistoryAPIView.as_view(), name='price_history'),
]
