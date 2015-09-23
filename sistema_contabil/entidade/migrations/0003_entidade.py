# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0002_delete_entidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='entidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf_cnpj', models.CharField(unique=True, max_length=18, verbose_name=b'Cpf / Cnpj:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('registro_geral', models.CharField(unique=True, max_length=12, verbose_name=b'Identidade:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('tipo_registro', models.CharField(default=b'C', max_length=1, choices=[(b'C', b'Cliente'), (b'F', b'Fornecedor'), (b'U', b'Funcion\xc3\xa1rio'), (b'O', b'Outro')], verbose_name=b'Tipo Registro:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome_razao', models.CharField(max_length=100, verbose_name=b'Nome Completo / Raz\xc3\xa3o Social:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('apelido_fantasia', models.CharField(max_length=50, verbose_name=b'Apelido / Nome Fantasia:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('inscricao_estadual', models.BooleanField(default=False, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Estadual:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('inscricao_municipal', models.BooleanField(default=False, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Municipal:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('inscricao_rural', models.BooleanField(default=False, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Rural:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('data_cadastro', models.DateField(auto_now=True)),
                ('desabilitado', models.BooleanField(default=False)),
            ],
        ),
    ]
