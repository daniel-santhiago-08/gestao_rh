from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PriceCrawlerList,
    PriceCrawlerMinList,
    PriceCrawlerEvolutionList,
    PriceCrawlerLineChart,
    PriceCrawlerPrintList,


)

urlpatterns = [
    path('hist/', PriceCrawlerList.as_view(), name='list_price_crawler_hist' ),
    path('hist-export-csv', PriceCrawlerList.export_csv, name='csv_hist'),

    # path('hist-search/', PriceCrawlerListSearch.as_view(), name='list_price_crawler_hist_search' ),
    path('min/', PriceCrawlerMinList.as_view(), name='list_price_crawler_min' ),
    path('min-export-csv/', PriceCrawlerMinList.export_csv, name='csv_min' ),

    path('evolution/', PriceCrawlerEvolutionList.as_view(), name='list_price_crawler_evolution' ),
    path('evolution-export-csv/', PriceCrawlerEvolutionList.export_csv, name='csv_evolution'),

    # path('pie-chart/', pie_chart, name='price_crawler_pie'),
    # path('line-chart/', line_chart, name='price_crawler_line')
    path('line-chart/', PriceCrawlerLineChart.as_view(), name='price_crawler_line'),

    path('prints/', PriceCrawlerPrintList.as_view(), name='list_price_crawler_prints' ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)