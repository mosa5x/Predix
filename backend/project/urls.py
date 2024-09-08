from django.contrib import admin
from django.urls import path
from marketing.views import (
    get_stock_data, get_all_stocks, get_stocks,
    get_commodities, get_commodity_data, get_all_commodities,
    get_cryptocurrencies, get_cryptocurrency_data, get_all_cryptocurrencies
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stocks/', get_all_stocks, name='get_all_stocks'),
    path('api/stocks/<str:stock>/', get_stock_data, name='get_stock_data'),
    path('api/stocklist/', get_stocks, name='get_stocks'),
    path('api/commodities/', get_all_commodities, name='get_all_commodities'),
    path('api/commodities/<str:commodity>/', get_commodity_data, name='get_commodity_data'),
    path('api/commoditylist/', get_commodities, name='get_commodities'),
    path('api/cryptocurrencies/', get_all_cryptocurrencies, name='get_all_cryptocurrencies'),
    path('api/cryptocurrencies/<str:crypto>/', get_cryptocurrency_data, name='get_cryptocurrency_data'),
    path('api/cryptocurrencylist/', get_cryptocurrencies, name='get_cryptocurrencies'),
]