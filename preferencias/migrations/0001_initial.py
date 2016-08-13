# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-07 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalarioMinimo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, default=0, error_messages={'invalid': 'Formato Inv\xe1lido!', 'required': 'Campo Obrigat\xf3rio!'}, max_digits=10, verbose_name='Valor:')),
                ('inicio_vigencia', models.DateField(blank=True, null=True, verbose_name='In\xedcio da vig\xeancia:')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
