# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0012_auto_20150908_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='bairro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_ibge', models.CharField(unique=True, max_length=10, verbose_name=b'C\xc3\xb3digo IBGE:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome', models.CharField(max_length=100, verbose_name=b'Bairro:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('municipio', models.ForeignKey(to='entidade.municipio')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bairro',
            unique_together=set([('nome', 'municipio')]),
        ),
    ]
