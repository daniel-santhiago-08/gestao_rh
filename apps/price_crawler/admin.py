from django.contrib import admin
from .models import PriceCrawler, PriceCrawlerEvolution


class PriceCrawlerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawler.objects.using('crawler').all()

class PriceCrawlerEvolutionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawlerEvolution.objects.using('crawler').all()

admin.site.register(PriceCrawler, PriceCrawlerAdmin)
admin.site.register(PriceCrawlerEvolution, PriceCrawlerEvolutionAdmin)