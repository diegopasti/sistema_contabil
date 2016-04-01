# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0026_auto_20151202_2338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localizacao',
            options={'verbose_name': 'Localizacao', 'verbose_name_plural': 'Localiza\xe7\xf5es'},
        ),
        migrations.AddField(
            model_name='entidade',
            name='numeracao_protocolo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='protocolo',
            name='numeracao_destinatario',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contato',
            name='tipo_contato',
            field=models.CharField(default=b'C', max_length=1, choices=[(b'C', b'CELULAR'), (b'F', b'COMERCIAL'), (b'R', b'RESIDENCIAL'), (b'O', b'OUTROS')], verbose_name=b'Tipo:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
        migrations.AlterField(
            model_name='entidade',
            name='tipo_registro',
            field=models.CharField(default=b'C', max_length=1, choices=[(b'C', b'CLIENTE'), (b'F', b'FORNECEDOR'), (b'U', b'FUNCIONARIO'), (b'O', b'OUTRO')], verbose_name=b'Tipo Registro:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
