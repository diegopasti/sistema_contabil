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
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cliente', models.CharField(choices=[('PF', 'PESSOA FISICA'), ('PJ', 'PESSOA JURIDICA')], default='PJ', error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Precisa ser Informado!'}, max_length=2, verbose_name='Tipo do Cliente:')),
                ('vigencia_inicio', models.DateField()),
                ('vigencia_fim', models.DateField()),
                ('taxa_honorario', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Honor\xe1rio:')),
                ('valor_honorario', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor:')),
                ('dia_vencimento', models.IntegerField(default=5, verbose_name='Dia do Vencimento:')),
                ('desconto_temporario', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Desconto Tempor\xe1rio:')),
                ('desconto_inicio', models.DateField(null=True)),
                ('desconto_fim', models.DateField(null=True)),
                ('desconto_indicacoes', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Desconto por Indica\xe7\xf5es:')),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('alterado_por', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='alterado_por', to='entidade.entidade')),
                ('cadastrado_por', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='cadastrado_por', to='entidade.entidade')),
                ('tipo_contrato', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='entidade.entidade')),
            ],
        ),
    ]
