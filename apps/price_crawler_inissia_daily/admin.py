from django.contrib import admin
from .models import PriceCrawlerInissia


class PriceCrawlerInissiaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawlerInissia.objects.using('crawler').all()


admin.site.register(PriceCrawlerInissia, PriceCrawlerInissiaAdmin)