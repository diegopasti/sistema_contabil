# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-05 20:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AtividadeEconomica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atividade', models.CharField(max_length=500, null=True, verbose_name=b'Atividade:')),
                ('desde', models.DateField(blank=True, null=True, verbose_name=b'Desde:')),
            ],
        ),
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_ibge', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=10, unique=True, verbose_name=b'Codigo IBGE:')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Bairro:')),
            ],
        ),
        migrations.CreateModel(
            name='contato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_contato', models.CharField(default=b'C', error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=10, verbose_name=b'Tipo:')),
                ('numero', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, verbose_name=b'Numero:')),
                ('nome_contato', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=50, verbose_name=b'Nome do Contato:')),
                ('cargo_setor', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=50, null=True, verbose_name=b'Cargo ou Setor:')),
                ('email', models.EmailField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=1, verbose_name=b'Tipo do Documento:')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Documento:')),
                ('vencimento', models.DateField(blank=True, null=True, verbose_name=b'Vencimento:')),
                ('senha', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Senha:')),
                ('data_cadastro', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('finalizado', models.BooleanField(default=False, verbose_name=b'Finalizado:')),
                ('data_finalizado', models.DateTimeField(null=True)),
                ('notificar_cliente', models.BooleanField(default=False, verbose_name=b'Notificar Cliente:')),
                ('prazo_notificar', models.IntegerField(blank=True, null=True, verbose_name=b'Prazo Notifica\xc3\xa7\xc3\xa3o:')),
            ],
        ),
        migrations.CreateModel(
            name='entidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=18, unique=True, verbose_name=b'Cnpj:')),
                ('nome_razao', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Raz\xc3\xa3o Social:')),
                ('apelido_fantasia', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=50, null=True, verbose_name=b'Nome Fantasia:')),
                ('registro_geral', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=12, null=True, verbose_name=b'Identidade:')),
                ('tipo_registro', models.CharField(default=b'C', error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=1, null=True, verbose_name=b'Tipo Registro:')),
                ('nascimento_fundacao', models.DateField(blank=True, null=True, verbose_name=b'Funda\xc3\xa7\xc3\xa3o:')),
                ('inscricao_estadual', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=9, null=True, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Estadual:')),
                ('inscricao_municipal', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, null=True, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Municipal:')),
                ('inscricao_produtor_rural', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, null=True, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Rural:')),
                ('inscricao_imovel_rural', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, null=True, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Im\xc3\xb3vel Rural:')),
                ('inscricao_junta_comercial', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, null=True, verbose_name=b'NIRE:')),
                ('nome_filial', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Identifica\xc3\xa7\xc3\xa3o Filial:')),
                ('natureza_juridica', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Natureza Jur\xc3\xaddica:')),
                ('regime_apuracao', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, null=True, verbose_name=b'Regime Tribut\xc3\xa1rio:')),
                ('regime_desde', models.DateField(blank=True, null=True, verbose_name=b'Desde:')),
                ('tipo_vencimento_iss', models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name=b'Tipo do Vencimento:')),
                ('data_vencimento_iss', models.DateField(blank=True, null=True, verbose_name=b'Vencimento (Anual):')),
                ('dia_vencimento_iss', models.IntegerField(blank=True, null=True, verbose_name=b'Vencimento (Mensal):')),
                ('taxa_iss', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name=b'Taxa:')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name=b'Observa\xc3\xa7\xc3\xb5es Administrativas')),
                ('notificacao_envio', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=1, null=True, verbose_name=b'Notificar Autom\xc3\xa1ticamente:')),
                ('notificacao_email', models.EmailField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Email do Respons\xc3\xa1vel:')),
                ('notificacao_responsavel', models.CharField(blank=True, error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Nome do Respons\xc3\xa1vel:')),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('numeracao_protocolo', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_ibge', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=2, unique=True, verbose_name=b'Codigo IBGE:')),
                ('sigla', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=2, unique=True, verbose_name=b'Sigla:')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, unique=True, verbose_name=b'Estado:')),
                ('regiao', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=20, verbose_name=b'Regi\xc3\xa3o:')),
            ],
        ),
        migrations.CreateModel(
            name='Localizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=5, null=True, verbose_name=b'Numero:')),
                ('complemento', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Complemento:')),
            ],
        ),
        migrations.CreateModel(
            name='localizacao_simples',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=8, verbose_name=b'Codigo Postal:')),
                ('logradouro', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Logradouro:')),
                ('numero', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=5, null=True, verbose_name=b'Numero:')),
                ('complemento', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, null=True, verbose_name=b'Complemento:')),
                ('bairro', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Bairro:')),
                ('codigo_ibge', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=7, verbose_name=b'Codigo Municipal:')),
                ('municipio', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Municipio:')),
                ('estado', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Estado:')),
                ('pais', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=30, verbose_name=b'Pa\xc3\xads:')),
            ],
        ),
        migrations.CreateModel(
            name='Logradouro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=8, unique=True, verbose_name=b'Codigo Postal:')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Endere\xc3\xa7o:')),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.Bairro')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_ibge', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=7, unique=True, verbose_name=b'Codigo Municipal:')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, verbose_name=b'Municipio:')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.Estado')),
            ],
        ),
        migrations.CreateModel(
            name='natureza_juridica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_natureza', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=5, unique=True, verbose_name=b'C\xc3\xb3digo:')),
                ('natureza_juridica', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, unique=True, verbose_name=b'Natureza Jur\xc3\xaddica:')),
            ],
        ),
        migrations.CreateModel(
            name='observacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now=True, verbose_name=b'Data:')),
                ('descricao', models.TextField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=500, verbose_name=b'Descri\xc3\xa7\xc3\xa3o: ')),
            ],
        ),
        migrations.CreateModel(
            name='OperacaoRestrita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[(b'ADD', b'ADI\xc3\x87\xc3\x83O'), (b'ALT', b'ALTERA\xc3\x87\xc3\x83O'), (b'DEL', b'EXCLUS\xc3\x83O'), (b'DES', b'DESATIVA\xc3\x87\xc3\x83O')], error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=3, verbose_name=b'Tipo:')),
                ('tabela', models.CharField(default=b'', error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=50, verbose_name=b'Tabela:')),
                ('descricao', models.TextField(default=b'', verbose_name=b'Descri\xc3\xa7\xc3\xa3o da Opera\xc3\xa7\xc3\xa3o: ')),
                ('justificativa', models.TextField(verbose_name=b'Justificativa: ')),
                ('data_operacao', models.DateTimeField(auto_now_add=True)),
                ('entidade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entidade.entidade')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=100, unique=True, verbose_name=b'Pa\xc3\xads:')),
                ('sigla', models.CharField(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, max_length=2, unique=True, verbose_name=b'Sigla:')),
            ],
            options={
                'verbose_name': 'Pa\xeds',
                'verbose_name_plural': 'Pa\xedses',
            },
        ),
        migrations.AddField(
            model_name='localizacao',
            name='logradouro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.Logradouro'),
        ),
        migrations.AddField(
            model_name='estado',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.Pais'),
        ),
        migrations.AddField(
            model_name='entidade',
            name='endereco',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='entidade.localizacao_simples'),
        ),
        migrations.AddField(
            model_name='entidade',
            name='responsavel_cliente',
            field=models.ForeignKey(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respondido_por', to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='entidade',
            name='supervisor_cliente',
            field=models.ForeignKey(error_messages={b'invalid': b'Formato Inv\xc3\xa1lido!', b'required': b'Campo Obrigat\xc3\xb3rio!'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supervisionado_por', to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='documento',
            name='criado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criado_por', to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='documento',
            name='entidade',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='documento',
            name='finalizado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finalizado_por', to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='contato',
            name='entidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.entidade'),
        ),
        migrations.AddField(
            model_name='bairro',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidade.Municipio'),
        ),
        migrations.AddField(
            model_name='atividadeeconomica',
            name='entidade',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='entidade.entidade'),
        ),
        migrations.AlterUniqueTogether(
            name='bairro',
            unique_together=set([('nome', 'municipio')]),
        ),
    ]
