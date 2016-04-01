# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0004_contato'),
    ]

    operations = [
        migrations.CreateModel(
            name='estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_ibge', models.CharField(unique=True, max_length=2, verbose_name=b'C\xc3\xb3digo IBGE:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('sigla', models.CharField(unique=True, max_length=2, verbose_name=b'Sigla:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name=b'Estado:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('regiao', models.CharField(unique=True, max_length=20, verbose_name=b'Regi\xc3\xa3o:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
        migrations.CreateModel(
            name='pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name=b'Estado:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('sigla', models.CharField(unique=True, max_length=2, verbose_name=b'Sigla:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
        migrations.DeleteModel(
            name='contato',
        ),
        migrations.AddField(
            model_name='estado',
            name='pais',
            field=models.ForeignKey(to='entidade.pais'),
        ),
    ]
