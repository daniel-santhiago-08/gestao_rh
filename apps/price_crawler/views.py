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



def create_csv(response, filename, dados):

    # response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
    fields = dados.first()._meta.fields
    field_name = [str(field).split('.')[-1] for field in fields]
    label_name = [str(field).split('.')[-1].capitalize() for field in fields]
    # Criação do CSV
    writer = csv.writer(response)
    # Adição do Header
    writer.writerow(label_name)
    # Adição dos dados
    data = serializers.serialize("python", dados)
    field_list = [field for field in field_name if field != 'id']
    for instance in data:
        csv_row = [instance['pk']]
        for field in field_list:
            csv_row.append(instance['fields'][field])
        writer.writerow(csv_row)

    return response

def get_fields_dictionary(fields):

    field_name = [str(field).split('.')[-1] for field in fields]
    label_name = [str(field).split('.')[-1].capitalize() for field in fields]
    fields_type_temp = [str(field.__class__).split('.')[-1].capitalize() for field in fields]
    fields_type = [str(field_type).split("'")[0] for field_type in fields_type_temp]
    ''' MAPEAMENTO DOS TIPOS DE DADOS PARA O TIPO DE INPUT '''
    type = ['text' if type == 'Charfield' else
            ('date' if type == 'Datefield' else 'num')

            for type in fields_type]

    fields_dictionary = {
        'field_name': field_name,
        'label_name': label_name,
        'fields_type': fields_type,
        'type': type,
    }

    return fields_dictionary


# def export_csv(self):
#     filename = 'Histórico'
#     dados = PriceCrawler.objects.using('crawler').all()
#     response = HttpResponse(content_type='text/csv')
#
#     response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
#     fields = dados.first()._meta.fields
#     field_name = [str(field).split('.')[-1] for field in fields]
#     label_name = [str(field).split('.')[-1].capitalize() for field in fields]
#
#     # Criação do CSV
#     writer = csv.writer(response)
#     # Adição do Header
#     writer.writerow(label_name)
#     # Adição dos dados
#     data = serializers.serialize("python", dados)
#     field_list = [field for field in field_name if field != 'id']
#     for instance in data:
#         csv_row = [instance['pk']]
#         for field in field_list:
#             csv_row.append(instance['fields'][field])
#         writer.writerow(csv_row)
#
#     # response = create_csv(response, filename, dados)
#     return response


class PriceCrawlerList(ListView):
    model = PriceCrawler
    DATABASE = 'crawler'
    rows_per_page = 10
    order_by = "-data_de_extracao"
    filtered_fields = ['produto','loja','data_de_extracao']
    field_names_order = ['id','loja','produto','data_de_extracao','preco']

    filename = 'Histórico'

    # @classmethod
    def export_csv(self):
        dados = PriceCrawler.objects.using('crawler').all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, 'Histórico', dados)
        return response

    def get_queryset(self):
        queryset = self.model.objects.using(self.DATABASE).all()
        min_date = queryset.order_by('data_de_extracao')[0].data_de_extracao
        max_date = queryset.order_by('-data_de_extracao')[0].data_de_extracao

        filtros = self.request.POST.get("filter_values")
        if filtros is None:
            print("none")
            queryset = queryset.filter(data_de_extracao__range=[min_date, max_date])
        else:
            filtros = json.loads(filtros)
            queryset = queryset.filter(produto__icontains=filtros['produto_search'])
            queryset = queryset.filter(loja__icontains=filtros['loja_search'])
            if filtros['data_de_extracao_inicial_search'] == '':
                queryset = queryset.filter(data_de_extracao__range=[min_date, max_date])
            else:
                queryset = queryset.filter(data_de_extracao__range=[
                              filtros['data_de_extracao_inicial_search'],
                              filtros['data_de_extracao_final_search']
                              ])

        # pesquisa_produto = self.request.POST.get("pesquisa_produto", "")
        # pesquisa_loja = self.request.POST.get("pesquisa_loja", "")
        # pesquisa_data_inicial = self.request.POST.get("pesquisa_data_inicial", "")
        # if pesquisa_data_inicial == '':
        #     pesquisa_data_inicial = min_date
        # pesquisa_data_final = self.request.POST.get("pesquisa_data_final", "")
        # if pesquisa_data_final == '':
        #     pesquisa_data_final = max_date


        order_by = self.request.POST.get("order_by", "data_de_extracao")

        queryset = queryset.order_by(order_by)

        return queryset



    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa','')
        if etapa_response == 'inicial':

            fields = self.get_queryset().first()._meta.fields
            fields_dictionary = get_fields_dictionary(fields)
            context = {
                'fields_dictionary': fields_dictionary,
                'rows_per_page': self.rows_per_page,
                'order_by': self.order_by,
                'filtered_fields': self.filtered_fields,
            }
            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
            return HttpResponse(context_json, content_type='application/json')

        else:

            querylist = list(self.get_queryset().values())
            first_page = "1"
            current_page = self.request.POST.get("current_page","1")

            if current_page == '':
                current_page = '1'
            previous_page = str(int(current_page) - 1)
            next_page = int(current_page) + 1
            next_page = str(next_page)
            total_rows = len(querylist)
            last_page = math.ceil(total_rows / self.rows_per_page)

            min_date = self.get_queryset().order_by('data_de_extracao')[0].data_de_extracao
            max_date = self.get_queryset().order_by('-data_de_extracao')[0].data_de_extracao

            fields = self.get_queryset().first()._meta.fields
            fields_list = [ str(field).split('.')[-1] for field in fields ]

            slice_start = (int(current_page) - 1) * self.rows_per_page + 0
            slice_end = (int(current_page) - 1) * self.rows_per_page + self.rows_per_page

            if self.field_names_order:
                field_names_order = self.field_names_order
            else:
                field_names_order = []

            context = {
                'object_list': querylist[slice_start:slice_end],
                'first_page': first_page,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
                'last_page': last_page,
                'min_date': min_date,
                'max_date': max_date,
                'fields_list': fields_list,
                'field_names_order': field_names_order,
            }

            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )

            return HttpResponse(context_json, content_type='application/json')







class PriceCrawlerMinList(ListView):
    model = PriceCrawlerMin
    DATABASE = 'crawler'
    rows_per_page = 10
    order_by = "-data_de_extracao"
    filtered_fields = ['produto','loja','data_de_extracao']
    field_names_order = ['id','loja','produto','data_de_extracao','preco']
    filename = 'PreçoMínimo'


    def export_csv(self):
        dados = PriceCrawlerMin.objects.using('crawler').all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, 'PreçoMínimo', dados)
        return response

    def get_queryset(self):
        queryset = self.model.objects.using(self.DATABASE).all()
        min_date = queryset.order_by('data_de_extracao')[0].data_de_extracao
        max_date = queryset.order_by('-data_de_extracao')[0].data_de_extracao
        pesquisa_produto = self.request.POST.get("pesquisa_produto", "")
        pesquisa_loja = self.request.POST.get("pesquisa_loja", "")
        pesquisa_data_inicial = self.request.POST.get("pesquisa_data_inicial", "")
        if pesquisa_data_inicial == '':
            pesquisa_data_inicial = min_date

        pesquisa_data_final = self.request.POST.get("pesquisa_data_final", "")
        if pesquisa_data_final == '':
            pesquisa_data_final = max_date
        order_by = self.request.POST.get("order_by", "data_de_extracao")
        queryset = queryset.filter(produto__icontains=pesquisa_produto)
        queryset = queryset.filter(loja__icontains=pesquisa_loja)
        # queryset = queryset.filter(data_de_extracao__range=[pesquisa_data_inicial,
        #                                                     pesquisa_data_final])

        queryset = queryset.filter(data_de_extracao__range=[str(pesquisa_data_inicial),
                                                            pesquisa_data_final])
        queryset = queryset.order_by(order_by)

        return queryset

    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa','')
        if etapa_response == 'inicial':

            fields = self.get_queryset().first()._meta.fields
            fields_dictionary = get_fields_dictionary(fields)
            context = {
                'fields_dictionary': fields_dictionary,
                'rows_per_page': self.rows_per_page,
                'order_by': self.order_by,
                'filtered_fields': self.filtered_fields,
            }

            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
            return HttpResponse(context_json, content_type='application/json')

        else:

            querylist = list(self.get_queryset().values())
            first_page = "1"
            current_page = self.request.POST.get("current_page","1")
            if current_page == '':
                current_page = '1'

            previous_page = str(int(current_page) - 1)

            next_page = int(current_page) + 1
            next_page = str(next_page)

            total_rows = len(querylist)
            last_page = math.ceil(total_rows / self.rows_per_page)

            min_date = self.get_queryset().order_by('data_de_extracao')[0].data_de_extracao
            max_date = self.get_queryset().order_by('-data_de_extracao')[0].data_de_extracao

            fields = self.get_queryset().first()._meta.fields
            fields_list = [ str(field).split('.')[-1] for field in fields ]

            slice_start = (int(current_page) - 1) * self.rows_per_page + 0
            slice_end = (int(current_page) - 1) * self.rows_per_page + self.rows_per_page

            if self.field_names_order:
                field_names_order = self.field_names_order
            else:
                field_names_order = []

            context = {
                'object_list': querylist[slice_start:slice_end],
                'first_page': first_page,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
                'last_page': last_page,
                'min_date': min_date,
                'max_date': max_date,
                'fields_list': fields_list,
                'field_names_order': field_names_order,
            }

            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )

            return HttpResponse(context_json, content_type='application/json')



class PriceCrawlerEvolutionList(ListView):
    model = PriceCrawlerEvolution
    DATABASE = 'crawler'
    rows_per_page = 7
    order_by = "-data_de_extracao"
    filtered_fields = ['data_de_extracao']
    field_names_order = ['id','data_de_extracao',
     'mini_me','essenza','inissia','mimo_cafeteira','pop_plus']
    filename = 'Evolução'

    def export_csv(self):
        dados = PriceCrawlerEvolution.objects.using('crawler').all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, 'Evolução', dados)
        return response

    def get_queryset(self):

        queryset = self.model.objects.using(self.DATABASE).all()
        min_date = queryset.order_by('data_de_extracao')[0].data_de_extracao
        max_date = queryset.order_by('-data_de_extracao')[0].data_de_extracao

        # pesquisa_produto = self.request.POST.get("pesquisa_produto", "")
        # pesquisa_loja = self.request.POST.get("pesquisa_loja", "")
        pesquisa_data_inicial = self.request.POST.get("pesquisa_data_inicial", "")
        if pesquisa_data_inicial == '':
            pesquisa_data_inicial = min_date
        pesquisa_data_final = self.request.POST.get("pesquisa_data_final", "")
        if pesquisa_data_final == '':
            pesquisa_data_final = max_date
        order_by = self.request.POST.get("order_by", "data_de_extracao")
        # queryset = queryset.filter(produto__icontains=pesquisa_produto)
        # queryset = queryset.filter(loja__icontains=pesquisa_loja)
        queryset = queryset.filter(data_de_extracao__range=[pesquisa_data_inicial,
                                                            pesquisa_data_final])
        queryset = queryset.order_by(order_by)

        return queryset

    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa', '')
        if etapa_response == 'inicial':

            fields = self.get_queryset().first()._meta.fields
            fields_dictionary = get_fields_dictionary(fields)
            context = {
                'fields_dictionary': fields_dictionary,
                'rows_per_page':self.rows_per_page,
                'order_by': self.order_by,
                'filtered_fields': self.filtered_fields,
            }
            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
            return HttpResponse(context_json, content_type='application/json')

        else:

            # rows_per_page = int(self.request.POST.get("rows_per_page", 5))
            querylist = list(self.get_queryset().values())
            first_page = "1"
            current_page = self.request.POST.get("current_page","1")

            if current_page == '':
                current_page = '1'

            previous_page = str(int(current_page) - 1)

            next_page = int(current_page) + 1
            next_page = str(next_page)

            total_rows = len(querylist)
            last_page = math.ceil(total_rows / self.rows_per_page)

            min_date = self.get_queryset().order_by('data_de_extracao')[0].data_de_extracao
            max_date = self.get_queryset().order_by('-data_de_extracao')[0].data_de_extracao

            fields = self.get_queryset().first()._meta.fields
            fields_list = [ str(field).split('.')[-1] for field in fields ]

            slice_start = (int(current_page) - 1) * self.rows_per_page + 0
            slice_end = (int(current_page) - 1) * self.rows_per_page + self.rows_per_page

            if self.field_names_order:
                field_names_order = self.field_names_order
            else:
                field_names_order = []

            context = {
                'object_list': querylist[slice_start:slice_end],
                # 'num': num,
                'first_page': first_page,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
                'last_page': last_page,
                'min_date': min_date,
                'max_date': max_date,
                'fields_list': fields_list,
                'field_names_order': field_names_order,
            }

            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )

            return HttpResponse(context_json, content_type='application/json')



class PriceCrawlerLineChart(ListView):
    model = PriceCrawlerEvolution
    template_name = 'price_crawler/line-chart.html'

    def post(self, request, *args, **kwargs):


        dados = PriceCrawlerEvolution.objects.using('crawler').all()
        datas = [obj.data_de_extracao.strftime("%Y") + '-' +
                 obj.data_de_extracao.strftime("%m") + '-' +
                 obj.data_de_extracao.strftime("%d")
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
    context_object_name = 'prints'
    DATABASE = 'crawler'
    rows_per_page = 6
    order_by = "-data"
    filtered_fields = ['loja','data']
    field_names_order = ['id','loja', 'produto','data']
    filename = 'Prints'

    def get_queryset(self):
        queryset = self.model.objects.using(self.DATABASE).all()
        min_date = queryset.order_by('data')[0].data
        max_date = queryset.order_by('-data')[0].data

        filtros = self.request.POST.get("filter_values")
        if filtros is None:
            print("none")
            queryset = queryset.filter(data__range=[min_date, max_date])
        else:
            filtros = json.loads(filtros)
            # queryset = queryset.filter(produto__icontains=filtros['produto_search'])
            queryset = queryset.filter(loja__icontains=filtros['loja_search'])
            if filtros['data_inicial_search'] == '':
                queryset = queryset.filter(data__range=[min_date, max_date])
            else:
                queryset = queryset.filter(data__range=[
                              filtros['data_inicial_search'],
                              filtros['data_final_search']
                              ])

        order_by = self.request.POST.get("order_by", "data")

        queryset = queryset.order_by(order_by)

        print(queryset)

        return queryset


    def post(self, request, *args, **kwargs):

        etapa_response = self.request.POST.get('etapa','')
        if etapa_response == 'inicial':

            fields = self.get_queryset().first()._meta.fields
            fields_dictionary = get_fields_dictionary(fields)
            context = {
                'fields_dictionary': fields_dictionary,
                'rows_per_page': self.rows_per_page,
                'order_by': self.order_by,
                'filtered_fields': self.filtered_fields,
            }
            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
            return HttpResponse(context_json, content_type='application/json')

        else:

            querylist = list(self.get_queryset().values())
            first_page = "1"
            current_page = self.request.POST.get("current_page","1")

            if current_page == '':
                current_page = '1'
            previous_page = str(int(current_page) - 1)
            next_page = int(current_page) + 1
            next_page = str(next_page)
            total_rows = len(querylist)
            last_page = math.ceil(total_rows / self.rows_per_page)

            min_date = self.get_queryset().order_by('data')[0].data
            max_date = self.get_queryset().order_by('-data')[0].data

            fields = self.get_queryset().first()._meta.fields
            fields_list = [ str(field).split('.')[-1] for field in fields ]

            slice_start = (int(current_page) - 1) * self.rows_per_page + 0
            slice_end = (int(current_page) - 1) * self.rows_per_page + self.rows_per_page

            if self.field_names_order:
                field_names_order = self.field_names_order
            else:
                field_names_order = []

            context = {
                'object_list': querylist[slice_start:slice_end],
                'first_page': first_page,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
                'last_page': last_page,
                'min_date': min_date,
                'max_date': max_date,
                'fields_list': fields_list,
                'field_names_order': field_names_order,
            }

            context_json = json.dumps(
                context,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )

            return HttpResponse(context_json, content_type='application/json')




#
# class Render:
#     @staticmethod
#     def render(path: str, params: dict, filename: str):
#         template = get_template(path)
#         html = template.render(params)
#         response = io.BytesIO()
#         pdf = pisaDocument(
#             io.BytesIO(html.encode("UTF-8")), response)
#         if not pdf.err:
#             response = HttpResponse(
#                 response.getvalue(), content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
#             return response
#         else:
#             return HttpResponse("Error Rendering PDF", status=400)
#
#
# class Pdf(View):
#
#     def get(self, request):
#         params = {
#             'today': 'Variavel today',
#             'sales': 'Variavel sales',
#             'request': request,
#         }
#
#         # print(PriceCrawlerList.get_queryset(self))
#
#         # return Render.render('funcionarios/relatorio.html', params, 'myfile')
#         return Render.render('price_crawler/relatorio.html', params, 'myfile')



class PriceCrawlerExportCSV(View):
    def get(self, request):
        filename = 'Histórico'
        dados = PriceCrawler.objects.using('crawler').all()
        response = HttpResponse(content_type='text/csv')
        response = create_csv(response, filename, dados)
        return response






def PriceCrawlerPrints(request):

    data = {}




    files = os.listdir(os.path.join(settings.MEDIA_ROOT, "documentos/"))
    print(files)
    data['files'] = files

    # data['usuario'] = request.user
    # return render(request, 'core/index.html', data)
    return render(request, 'price_crawler/prints.html', data)



