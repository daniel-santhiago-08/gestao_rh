import csv
import io
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse, Http404
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import _
from django.template.loader import get_template
from django.core import serializers
from .filters import PriceCrawlerFilter
from django_filters.views import FilterView
import datetime
import json
import math
import os
from datetime import datetime, timedelta
from django.db.models import Count, Min, Sum, Avg, Max
from .models import PriceCrawler, PriceCrawlerMin, PriceCrawlerEvolution, PriceCrawlerPrint
from django.views.generic import ListView
from django import forms
from django.core import serializers
from django.contrib.admin.options import get_content_type_for_model
from gestao_rh import settings

from apps.core.views_functions import *



class PriceCrawlerList(ListView):
    ''' Database utilizado em settings.py '''
    DATABASE = 'machines_crawler'
    ''' Modelo do Django '''
    model = PriceCrawler
    ''' Ordem das colunas  '''
    field_names_order = ['id', 'loja', 'produto', 'data_extracao', 'preco']
    ''' Ordenação inicial:   
        Ordem Descrescente -> Sufixo '-'  +  Nome do campo   
        Ordem Crescente ->                   Nome do campo  
    '''
    order_by = "-data_extracao"
    ''' Campo de Data: Nome do campo '''
    date_field = 'data_extracao'
    ''' Lista de Filtros: Nome dos campos que serão apresentados nos filtros '''
    filtered_fields = ['produto', 'loja', 'data_extracao']
    ''' Número de registros por página '''
    rows_per_page = 10
    ''' Tipo de objeto que será preenchido pelo Queryset '''
    fillObject = 'table'  # 'table' or 'image'
    ''' Nome do Arquivo que será exportado '''
    filename = 'Histórico'

    # @classmethod
    # def export_csv(self):
    #     dados = PriceCrawler.objects.using('machines_crawler').all()
    #     response = HttpResponse(content_type='text/csv')
    #     response = create_csv(response, 'Histórico', dados)
    #     return response



    def get_queryset(self):
        return filter_queryset(self)

    def post(self, request, *args, **kwargs):

        # etapa_response = self.request.POST.get('etapa','')
        if self.request.POST.get('etapa','') == 'inicial':
            context_json = initial_post(self)
        else:
            context_json = ajax_post(self)

        return HttpResponse(context_json, content_type='application/json')

    def export_csv(self):
        cls = PriceCrawlerList()
        dados = cls.model.objects.using(cls.DATABASE).all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, cls.filename, dados)
        return response




class PriceCrawlerMinList(ListView):
    model = PriceCrawlerMin
    DATABASE = 'machines_crawler'
    rows_per_page = 10
    order_by = "-data_extracao"
    filtered_fields = ['produto','loja','data_extracao']
    field_names_order = ['id','loja','produto','data_extracao','preco']
    date_field = 'data_extracao'
    filename = 'PreçoMínimo'
    fillObject = 'table'  # 'table' or 'image'

    def export_csv(self):
        cls = PriceCrawlerMinList()
        dados = cls.model.objects.using(cls.DATABASE).all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, cls.filename, dados)
        return response

    def get_queryset(self):

        return filter_queryset(self)

    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa','')
        if etapa_response == 'inicial':
            context_json = initial_post(self)
        else:
            context_json = ajax_post(self)

        return HttpResponse(context_json, content_type='application/json')


class PriceCrawlerEvolutionList(ListView):
    model = PriceCrawlerEvolution
    DATABASE = 'machines_crawler'
    rows_per_page = 7
    order_by = "-data_extracao"
    filtered_fields = ['data_extracao']
    field_names_order = ['id','data_extracao',
     'mini_me','essenza','inissia','mimo_cafeteira','pop_plus']
    date_field = 'data_extracao'
    filename = 'Evolução'
    fillObject = 'table'  # 'table' or 'image'

    def export_csv(self):
        cls = PriceCrawlerEvolutionList()
        dados = cls.model.objects.using(cls.DATABASE).all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, cls.filename, dados)
        return response

    def get_queryset(self):

        return filter_queryset(self)

    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa', '')
        if etapa_response == 'inicial':
            context_json = initial_post(self)
        else:
            context_json = ajax_post(self)

        return HttpResponse(context_json, content_type='application/json')


class PriceCrawlerLineChart(ListView):
    model = PriceCrawlerEvolution
    template_name = 'price_crawler/line-chart.html'

    def post(self, request, *args, **kwargs):

        dados = PriceCrawlerEvolution.objects.using('machines_crawler').all()
        datas = [obj.data_extracao.strftime("%Y") + '-' +
                 obj.data_extracao.strftime("%m") + '-' +
                 obj.data_extracao.strftime("%d")
                 for obj in dados]

        mini_me = [int(obj.mini_me) for obj in dados]
        essenza = [int(obj.essenza) for obj in dados]
        inissia = [int(obj.inissia) for obj in dados]
        mimo_cafeteira = [int(obj.mimo_cafeteira) for obj in dados]
        pop_plus = [int(obj.pop_plus) for obj in dados]

        context = {
            'datas': json.dumps(datas),
            'mini_me': json.dumps(mini_me),
            'essenza': json.dumps(essenza),
            'inissia': json.dumps(inissia),
            'mimo_cafeteira': json.dumps(mimo_cafeteira),
            'pop_plus': json.dumps(pop_plus),
        }

        context_json = json.dumps(
            context,
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder
        )

        return HttpResponse(context_json, content_type='application/json')



class PriceCrawlerPrintList(ListView):
    model = PriceCrawlerPrint
    DATABASE = 'machines_crawler'
    rows_per_page = 6
    order_by = "-data"
    filtered_fields = ['produto','loja','data']
    field_names_order = ['id','loja', 'produto','data']
    date_field = 'data'
    filename = 'Prints'
    fillObject = 'image' # 'table' or 'image'

    def get_queryset(self):

        return filter_queryset(self)


    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa','')
        if etapa_response == 'inicial':
            context_json = initial_post(self)
        else:
            context_json = ajax_post(self)

        return HttpResponse(context_json, content_type='application/json')


# class PriceCrawlerExportCSV(View):
#     def get(self, request):
#         filename = 'Histórico'
#         dados = PriceCrawler.objects.using('machines_crawler').all()
#         response = HttpResponse(content_type='text/csv')
#         response = create_csv(response, filename, dados)
#         return response
#

