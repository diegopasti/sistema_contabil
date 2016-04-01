# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0018_auto_20150923_0357'),
    ]

    operations = [
        migrations.CreateModel(
            name='observacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(auto_now=True, verbose_name=b'Data:')),
                ('titulo', models.CharField(max_length=100, verbose_name=b'T\xc3\xadtulo: ', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('descricao', models.TextField(max_length=500, verbose_name=b'Descri\xc3\xa7\xc3\xa3o: ', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
    ]
