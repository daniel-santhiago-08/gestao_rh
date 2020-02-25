from django.shortcuts import render
from .models import PriceCrawlerInissia
from django.views.generic import ListView


class PriceCrawlerList(ListView):
    model = PriceCrawlerInissia

    # def get_queryset(self, request):
    #     return PriceCrawlerInissia.objects.using('crawler').all()

    def get_queryset(self):
        queryset = PriceCrawlerInissia.objects.using('crawler').all()
        # queryset = Funcionario.objects.filter(empresa=empresa_logada)
        return queryset