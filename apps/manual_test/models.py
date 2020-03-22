from django.db import models

# Create your models here.

class ManualProductIds(models.Model):

    categoria = models.CharField(max_length=30)
    capsula = models.CharField(max_length=30)
    productid = models.CharField(max_length=10)
    tipo = models.CharField(max_length=30)
    multiplicador_dose = models.DecimalField(decimal_places=2, max_digits=5)
    multiplicador_capsula = models.DecimalField(decimal_places=2, max_digits=5)
    multiplicador_caixa = models.DecimalField(decimal_places=2, max_digits=5)
    child_productid = models.CharField(max_length=50)
    sku_ga = models.CharField(max_length=50)
    produto_ga = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'manual_productids'

    def __str__(self):
        return str(self.productid) + ' - ' + str(self.sku_GA)