from django.urls import path
from .views import (
    PriceCrawlerList,
    PriceCrawlerMinList,
    PriceCrawlerEvolutionList,
    PriceCrawlerListFilterClass,
    # pie_chart,
    line_chart,
    search
)

urlpatterns = [
    path('hist/', PriceCrawlerList.as_view(), name='list_price_crawler_hist' ),
    # path('hist/', search, name='list_price_crawler_hist' ),
    # path(r'^search/$', search, name='list_price_crawler_hist' ),
    path('min/', PriceCrawlerMinList.as_view(), name='list_price_crawler_min' ),
    path('evolution/', PriceCrawlerEvolutionList.as_view(), name='list_price_crawler_evolution' ),
    # path('pie-chart/', pie_chart, name='price_crawler_pie'),
    path('line-chart/', line_chart, name='price_crawler_line')

]