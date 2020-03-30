from django.core.validators import MinValueValidator
from django.db import models


class PriceCrawler(models.Model):

    produto = models.CharField(max_length=50)
    data_extracao = models.DateField()
    loja = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'price_crawler_hist'

class PriceCrawlerMin(models.Model):

    produto = models.CharField(max_length=50)
    data_extracao = models.DateField()
    loja = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'price_crawler_min'


class PriceCrawlerEvolution(models.Model):

    data_extracao = models.DateField()
    mini_me = models.DecimalField(decimal_places=2, max_digits=7)
    essenza = models.DecimalField(decimal_places=2, max_digits=7)
    inissia = models.DecimalField(decimal_places=2, max_digits=7)
    mimo_cafeteira = models.DecimalField(decimal_places=2, max_digits=7)
    pop_plus = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'price_crawler_evolution'

class PriceCrawlerPrint(models.Model):

    loja = models.CharField(max_length=50)
    produto = models.CharField(max_length=50)
    data = models.DateField()
    # photo = models.BinaryField(blank=True, null=True)
    # photo = models.ImageField(upload_to=b'screenshots', blank=True, null=True)
    url = models.CharField(max_length=100)
    # file_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'machine_print'
