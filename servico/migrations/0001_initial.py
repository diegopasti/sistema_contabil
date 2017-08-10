# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-10 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entidade', '0003_auto_20170206_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=100, null=True, verbose_name='Nome:')),
                ('descricao', models.TextField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=500, null=True, verbose_name='Descri\xe7\xe3o:')),
                ('servicos', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=500, null=True, verbose_name='Servi\xe7os:')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('alterado_por', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='plano_alterado_por', to='entidade.entidade')),
                ('cadastrado_por', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='plano_cadastrado_por', to='entidade.entidade')),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=100, null=True, verbose_name='Nome:')),
                ('descricao', models.TextField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=500, null=True, verbose_name='Descri\xe7\xe3o:')),
            ],
        ),
    ]
