from django.db import models


class PriceCrawlerInissia(models.Model):

    produto = models.CharField(max_length=50)
    data_de_extracao = models.DateField()
    loja = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        managed = False
        db_table = 'Price_Crawler_Inissia_dayly'


    # def __str__(self):
    #     return self.produto + '_' + self.loja + '_' +str(self.data_de_extracao)