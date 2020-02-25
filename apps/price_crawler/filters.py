from .models import PriceCrawler, PriceCrawlerMin, PriceCrawlerEvolution
import django_filters


class PriceCrawlerFilter(django_filters.FilterSet):

    CHOICES = (
        ('crescente','Crescente'),
        ('decrescente','Decrescente')
    )
    ordering = django_filters.ChoiceFilter(label='Ordenação por Data',
                                           choices=CHOICES,
                                           method='filter_by_order')

    class Meta:
        model = PriceCrawler
        # fields = ['produto']
        fields = {
            'produto': ['icontains'],
            'loja': ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'data_de_extracao' if value == 'crescente' else '-data_de_extracao'
        return queryset.order_by(expression)

