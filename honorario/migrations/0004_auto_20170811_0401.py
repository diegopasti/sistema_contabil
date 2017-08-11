# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honorario', '0003_auto_20170811_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='taxa_honorario',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Honor\xe1rio:'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='valor_honorario',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Valor:'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='vigencia_fim',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='vigencia_inicio',
            field=models.DateField(null=True),
        ),
    ]