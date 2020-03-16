from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from .models import ManualProductIds
from django.views.generic import ListView

from apps.core.views_functions import *


class ManualProductIdsList(ListView):
    ''' Database utilizado em settings.py '''
    DATABASE = 'manual'
    ''' Modelo do Django '''
    model = ManualProductIds
    ''' Ordem das colunas  '''
    field_names_order = ['id',
     'categoria', 'capsula', 'productid',
     'tipo', 'multiplicador_dose', 'multiplicador_capsula',
     'multiplicador_caixa', 'child_productid', 'sku_GA',
     'produto_GA'
                         ]
    ''' Ordenação inicial:   
        Ordem Descrescente -> Sufixo '-'  +  Nome do campo   
        Ordem Crescente ->                   Nome do campo  
    '''
    order_by = "productid"
    ''' Campo de Data: Nome do campo '''
    date_field = ''
    ''' Lista de Filtros: Nome dos campos que serão apresentados nos filtros '''
    filtered_fields = ['categoria', 'capsula', 'productid']
    ''' Número de registros por página '''
    rows_per_page = 7
    ''' Tipo de objeto que será preenchido pelo Queryset '''
    fillObject = 'table'  # 'table' or 'image'
    ''' Nome do Arquivo que será exportado '''
    filename = 'manual_product_ids'

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
        cls = ManualProductIdsList()
        dados = cls.model.objects.using(cls.DATABASE).all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, cls.filename, dados)
        return response

