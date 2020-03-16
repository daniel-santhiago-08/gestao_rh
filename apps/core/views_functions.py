import csv

from django.core.serializers.json import DjangoJSONEncoder

import json
import math

from django.core import serializers




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


def filter_queryset(self):

    queryset = self.model.objects.using(self.DATABASE).all()

    date_field = self.date_field
    if len(date_field) > 0 :
        min_date = queryset.order_by(date_field).values()[0][date_field]
        max_date = queryset.order_by('-'+date_field).values()[0][date_field]

    filtros = self.request.POST.get("filter_values")

    if filtros is None:
        if len(date_field) > 0:
            field_query = self.date_field + '__range'
            queryset = queryset.filter(**{field_query: [min_date, max_date]})
    else:
        filtros = json.loads(filtros)

        #######################################################################

        fields_filters = []
        for filter_name in filtros:
            field_name = filter_name.replace('_search','').replace('_inicial','').replace('_final','')
            fields_filters.append(field_name)

        field_filters = list(set(fields_filters))
        for field_filter in field_filters:
            if field_filter == self.date_field:
                field_query = field_filter + '__range'
                if filtros[self.date_field + '_inicial_search'] == '':
                    queryset = queryset.filter(**{field_query: [min_date, max_date]})
                else:
                    queryset = queryset.filter(**{field_query: [
                        filtros[self.date_field + '_inicial_search'],
                        filtros[self.date_field + '_final_search']
                    ]})

            else:
                field_query = field_filter + '__icontains'
                field_value = filtros[field_filter+'_search']
                queryset = queryset.filter(**{field_query: field_value })

        #######################################################################


        # queryset = queryset.filter(produto__icontains=filtros['produto_search'])
        # queryset = queryset.filter(loja__icontains=filtros['loja_search'])
        # if filtros[self.date_field+'_inicial_search'] == '':
        #     queryset = queryset.filter(data_de_extracao__range=[min_date, max_date])
        # else:
        #     queryset = queryset.filter(data_de_extracao__range=[
        #                   filtros[self.date_field+'_inicial_search'],
        #                   filtros[self.date_field+'_final_search']
        #                   ])

    if len(date_field) > 0:
        order_by = self.request.POST.get("order_by", self.date_field)
    else:
        order_by = self.request.POST.get("order_by","id")

    queryset = queryset.order_by(order_by)

    return queryset


def initial_post(self):
    fields = self.get_queryset().first()._meta.fields
    fields_dictionary = get_fields_dictionary(fields)
    context = {
        'fields_dictionary': fields_dictionary,
        'rows_per_page': self.rows_per_page,
        'order_by': self.order_by,
        'filtered_fields': self.filtered_fields,
        'fillObject': self.fillObject,
        'date_field': self.date_field
    }
    context_json = json.dumps(
        context,
        sort_keys=True,
        indent=1,
        cls=DjangoJSONEncoder
    )

    return context_json

def ajax_post(self):

    date_field = self.date_field
    if len(date_field) > 0:
        min_date = self.get_queryset().order_by(date_field).values()[0][date_field]
        max_date = self.get_queryset().order_by('-'+date_field).values()[0][date_field]
    else:
        min_date = ''
        max_date = ''

    querylist = list(self.get_queryset().values())
    first_page = "1"
    current_page = self.request.POST.get("current_page", "1")

    if current_page == '':
        current_page = '1'
    previous_page = str(int(current_page) - 1)
    next_page = int(current_page) + 1
    next_page = str(next_page)
    total_rows = len(querylist)
    last_page = math.ceil(total_rows / self.rows_per_page)

    fields = self.get_queryset().first()._meta.fields
    fields_list = [str(field).split('.')[-1] for field in fields]

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

    return context_json
