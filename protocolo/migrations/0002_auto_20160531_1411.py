# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-31 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocolo',
            name='emitido_por',
            field=models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=100, null=True, verbose_name=b'Recebido por:'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='data_recebimento',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='hora_recebimento',
            field=models.TimeField(blank=True),
        ),
    ]