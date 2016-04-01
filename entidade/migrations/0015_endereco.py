# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0014_entidade_nascimento_fundacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='endereco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cep', models.CharField(unique=True, max_length=7, verbose_name=b'C\xc3\xb3digo Postal:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome', models.CharField(max_length=100, verbose_name=b'Bairro:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('bairro', models.ForeignKey(to='entidade.bairro')),
            ],
        ),
    ]
