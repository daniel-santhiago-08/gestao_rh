from django.urls import path
from .views import (
    PriceCrawlerList
)

urlpatterns = [
    path('', PriceCrawlerList.as_view(), name='list_price_crawler' ),

]