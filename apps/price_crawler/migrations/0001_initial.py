# Generated by Django 3.0.3 on 2020-02-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceCrawler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', models.CharField(max_length=50)),
                ('data_de_extracao', models.DateField()),
                ('loja', models.CharField(max_length=50)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
            options={
                'db_table': 'Price_Crawler_Hist',
            },
        ),
    ]
