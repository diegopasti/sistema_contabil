# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honorario', '0002_auto_20170811_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='dia_vencimento',
            field=models.CharField(default=5, max_length=2, null=True, verbose_name='Dia do Vencimento:'),
        ),
    ]
