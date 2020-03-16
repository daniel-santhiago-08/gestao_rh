from django.contrib import admin
from .models import ManualProductIds


class ManualProductIdsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return ManualProductIds.objects.using('manual').all()


admin.site.register(ManualProductIds, ManualProductIdsAdmin)