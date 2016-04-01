# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0020_remove_observacao_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='natureza_juridica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_natureza', models.CharField(unique=True, max_length=5, verbose_name=b'C\xc3\xb3digo:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('natureza_juridica', models.CharField(unique=True, max_length=100, verbose_name=b'Natureza Jur\xc3\xaddica:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
    ]
