# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0022_auto_20150930_0436'),
    ]

    operations = [
        migrations.CreateModel(
            name='localizacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=5, verbose_name=b'N\xc3\xbamero:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name=b'Complemento:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('cep', models.ForeignKey(to='entidade.endereco')),
                ('entidade', models.ForeignKey(to='entidade.entidade')),
            ],
        ),
    ]
