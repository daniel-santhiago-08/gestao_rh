from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ManualProductIdsList

)

urlpatterns = [
    path('product-ids/', ManualProductIdsList.as_view(), name='list_manual_product_ids' ),
    path('product-ids-export-csv', ManualProductIdsList.export_csv, name='csv_product'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)