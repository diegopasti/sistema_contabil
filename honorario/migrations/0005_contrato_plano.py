# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 04:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0001_initial'),
        ('honorario', '0004_auto_20170811_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='plano',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='servico.Plano'),
        ),
    ]