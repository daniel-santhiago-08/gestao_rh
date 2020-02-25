# Generated by Django 3.0.3 on 2020-02-24 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_crawler', '0002_auto_20200223_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceCrawlerEvolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_de_extracao', models.DateField()),
                ('essenza', models.DecimalField(decimal_places=2, max_digits=7)),
                ('inissia', models.DecimalField(decimal_places=2, max_digits=7)),
                ('mimo_cafeteira', models.DecimalField(decimal_places=2, max_digits=7)),
                ('pop_plus', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
            options={
                'db_table': 'Price_Crawler_Evolution',
                'managed': False,
            },
        ),
    ]
