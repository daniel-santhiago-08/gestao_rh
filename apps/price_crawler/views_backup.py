from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views import View

from .filters import PriceCrawlerFilter
from django_filters.views import FilterView
import datetime
import json

from .models import PriceCrawler, PriceCrawlerMin, PriceCrawlerEvolution
from django.views.generic import ListView


class PriceCrawlerList(ListView):
    model = PriceCrawler
    paginate_by = 10
    template_name = 'price_crawler/pricecrawler_list.html'
    # context_object_name = 'object_list'


    def get_queryset(self):
        queryset = PriceCrawler.objects.using('crawler').all()
        # if self.request.POST:
        #     print("POST")
        #     pesquisa = self.request.POST.get("pesquisa", "")
        #     queryset = queryset.filter(produto__icontains=pesquisa)

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = PriceCrawler.objects.using('crawler').all()
    #     pesquisa = self.request.POST.get("pesquisa", "")
    #     queryset = queryset.filter(produto__icontains=pesquisa)
    #     context['object_list'] = queryset
    #     return context

    def post(self, request, *args, **kwargs):

        # self.get_context_data()
        # self.get_queryset()
        response = json.dumps(
            {'mensagem': 'Requisicao executada',
             }
        )
        return HttpResponse(response, content_type='application/json')





# class PriceCrawlerListSearch(View):
#
#     def post(self, *args, **kwargs):
#         print(self.request.POST.get("pesquisa", ""))
#         pesquisa = self.request.POST.get("pesquisa", "")
#         qs = PriceCrawler.objects.using('crawler').all()
#         queryList = qs.filter(produto__icontains=pesquisa)
#         print(queryList)
#
#
#         response = json.dumps(
#             {'mensagem': 'Requisicao executada',
#              }
#         )
#
#         return HttpResponse(response, content_type='application/json')
#

# class PriceCrawlerListFilterClass(FilterView):
#     model = PriceCrawler
#     paginate_by = 10
#     context_object_name = 'object_list'
#     filterset_class  = PriceCrawlerFilter
#     template_name = 'price_crawler/pricecrawler_list.html'
#
#     def get_queryset(self ):
#         queryset = PriceCrawler.objects.using('crawler').all()
#         price_crawler_filter = PriceCrawlerFilter(self.request.GET, queryset=queryset)
#         return price_crawler_filter
#
#
#
# def search(request):
#     queryset = PriceCrawler.objects.using('crawler').all()
#     price_crawler_filter = PriceCrawlerFilter(request.GET, queryset=queryset)
#     paginate_by = 10
#     return render(request, 'price_crawler/pricecrawler_list.html', {'object_list': price_crawler_filter})




class PriceCrawlerMinList(ListView):
    model = PriceCrawlerMin
    paginate_by = 10

    def get_queryset(self):
        queryset = PriceCrawlerMin.objects.using('crawler').all()
        return queryset

class PriceCrawlerEvolutionList(ListView):
    model = PriceCrawlerEvolution
    paginate_by = 10

    def get_queryset(self):
        queryset = PriceCrawlerEvolution.objects.using('crawler').all()
        return queryset




def line_chart(request):

    dados = PriceCrawlerEvolution.objects.using('crawler').all()
    print(dados)
    datas = [obj.data_de_extracao.strftime("%Y")+'-'+
             obj.data_de_extracao.strftime("%m") +'-'+
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

    print(context)


    return render(request, 'price_crawler/line-chart.html', context)



    # return render(request, 'price_crawler/pie-chart.html',response)

# def line_chart(request):
#     labels = []
#     data = []
#
#     dados = PriceCrawlerMin.objects.using('crawler').all()
#     # queryset = PriceCrawlerMin.objects.order_by('-population')[:5]
#     inissia = dados.filter(produto='inissia')
#     print(dados)
#     print(inissia)
#     for produto in inissia:
#         print(produto.produto)
#         labels.append(produto.data_de_extracao)
#         data.append(produto.preco)
#
#     # data = [{"x": x, "y": y} for x, y in zip(x, y)]
#     data = {
#         'labels': labels,
#         'data': data,
#     }
#
#     print(data)
#
#
#     return render(request, 'price_crawler/line-chart.html',data)



