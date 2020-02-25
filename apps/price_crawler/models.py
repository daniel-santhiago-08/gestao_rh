from django.core.validators import MinValueValidator
from django.db import models


class PriceCrawler(models.Model):

    produto = models.CharField(max_length=50)
    data_de_extracao = models.DateField()
    loja = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'Price_Crawler_Hist'

class PriceCrawlerMin(models.Model):

    produto = models.CharField(max_length=50)
    data_de_extracao = models.DateField()
    loja = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'Price_Crawler_Min_Price'


class PriceCrawlerEvolution(models.Model):

    data_de_extracao = models.DateField()
    mini_me = models.DecimalField(decimal_places=2, max_digits=7)
    essenza = models.DecimalField(decimal_places=2, max_digits=7)
    inissia = models.DecimalField(decimal_places=2, max_digits=7)
    mimo_cafeteira = models.DecimalField(decimal_places=2, max_digits=7)
    pop_plus = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'Price_Crawler_Evolution'
