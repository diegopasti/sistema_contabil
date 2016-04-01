# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0003_entidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='contato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_contato', models.CharField(default=b'C', max_length=1, choices=[(b'C', b'Celular'), (b'F', b'Comercial'), (b'R', b'Residencial'), (b'O', b'Outros')], verbose_name=b'Tipo:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('ddd', models.IntegerField()),
                ('numero', models.CharField(max_length=9, verbose_name=b'Numero:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome_contato', models.CharField(max_length=50, verbose_name=b'Nome do Contato:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('cargo_setor', models.CharField(max_length=50, null=True, verbose_name=b'Cargo ou Setor:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('email', models.EmailField(max_length=100, null=True, error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
            ],
        ),
    ]
