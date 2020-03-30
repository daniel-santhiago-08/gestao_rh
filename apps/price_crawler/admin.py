from django.contrib import admin
from .models import PriceCrawler, PriceCrawlerEvolution, PriceCrawlerPrint


class PriceCrawlerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawler.objects.using('machines_crawler').all()

class PriceCrawlerEvolutionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawlerEvolution.objects.using('machines_crawler').all()

class PriceCrawlerPrintAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return PriceCrawlerPrint.objects.using('crawler').all()

admin.site.register(PriceCrawler, PriceCrawlerAdmin)
admin.site.register(PriceCrawlerEvolution, PriceCrawlerEvolutionAdmin)
admin.site.register(PriceCrawlerPrint, PriceCrawlerPrintAdmin)