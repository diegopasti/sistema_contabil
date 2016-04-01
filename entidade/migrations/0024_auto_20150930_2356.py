# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0023_localizacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='item_protocolo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=100, verbose_name=b'Item:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('mes_referencia', models.DateField(null=True, verbose_name=b'M\xc3\xaas de Refer\xc3\xaancia:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('vencimento', models.DateField(null=True, verbose_name=b'Vencimento:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('valor', models.DateField(null=True, verbose_name=b'Valor:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('complemento', models.TextField(max_length=500, verbose_name=b'Descri\xc3\xa7\xc3\xa3o:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
        migrations.CreateModel(
            name='protocolo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_emissao', models.DateField(auto_now=True)),
                ('destinatario', models.ForeignKey(related_name='entidade_destinataria', to='entidade.entidade')),
                ('emissor', models.ForeignKey(related_name='entidade_emissora', to='entidade.entidade')),
            ],
        ),
        migrations.AddField(
            model_name='item_protocolo',
            name='protocolo',
            field=models.ForeignKey(to='entidade.protocolo'),
        ),
    ]
