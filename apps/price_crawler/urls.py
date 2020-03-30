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

from .views_old import (
    PriceCrawlerList_old,
    PriceCrawlerMinList_old,
    PriceCrawlerEvolutionList_old,
    PriceCrawlerLineChart_old,
    PriceCrawlerPrintList_old,
)


urlpatterns = [
    path('hist/', PriceCrawlerList.as_view(), name='list_price_crawler_hist' ),
    path('hist-export-csv', PriceCrawlerList.export_csv, name='csv_hist'),
    path('min/', PriceCrawlerMinList.as_view(), name='list_price_crawler_min' ),
    path('min-export-csv/', PriceCrawlerMinList.export_csv, name='csv_min' ),
    path('evolution/', PriceCrawlerEvolutionList.as_view(), name='list_price_crawler_evolution' ),
    path('evolution-export-csv/', PriceCrawlerEvolutionList.export_csv, name='csv_evolution'),
    path('line-chart/', PriceCrawlerLineChart.as_view(), name='price_crawler_line'),
    path('prints/', PriceCrawlerPrintList.as_view(), name='list_price_crawler_prints' ),

    path('hist_old/', PriceCrawlerList_old.as_view(), name='list_price_crawler_hist_old'),
    path('hist-export-csv_old', PriceCrawlerList_old.export_csv, name='csv_hist_old'),
    path('min_old/', PriceCrawlerMinList_old.as_view(), name='list_price_crawler_min_old' ),
    path('min-export-csv_old/', PriceCrawlerMinList_old.export_csv, name='csv_min_old' ),
    path('evolution_old/', PriceCrawlerEvolutionList_old.as_view(), name='list_price_crawler_evolution_old' ),
    path('evolution-export-csv_old/', PriceCrawlerEvolutionList_old.export_csv, name='csv_evolution_old'),
    path('line-chart_old/', PriceCrawlerLineChart_old.as_view(), name='price_crawler_line_old'),
    path('prints_old/', PriceCrawlerPrintList_old.as_view(), name='list_price_crawler_prints_old' ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)