# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from entidade.formularios import MENSAGENS_ERROS
from entidade.models import entidade
from django.db import models

from servico.models import Plano


class Contrato(models.Model):
    plano = models.ForeignKey(Plano, default=1)

    cliente = models.ForeignKey(entidade, default=1)
    opcoes_tipos_clientes = (('PF', 'PESSOA FISICA'), ('PJ', 'PESSOA JURIDICA'),)
    tipo_cliente  = models.CharField("Tipo do Cliente:",max_length=2,null=False,default='PJ',choices = opcoes_tipos_clientes,error_messages=MENSAGENS_ERROS)

    vigencia_inicio = models.DateField(null=True)
    vigencia_fim    = models.DateField(null=True)

    taxa_honorario  = models.DecimalField("Honorário:", max_digits=5, decimal_places=2, null=True,blank=False)
    valor_honorario = models.DecimalField("Valor:", max_digits=6, decimal_places=2, null=True,blank=False)
    dia_vencimento  = models.CharField("Dia do Vencimento",null=True,default=5,max_length=2)
    data_vencimento = models.DateField("Data de Vencimento",null=True)

    desconto_temporario = models.DecimalField("Desconto Temporário:", max_digits=5,default=0, decimal_places=2, null=True,blank=True)
    desconto_inicio = models.DateField(null=True)
    desconto_fim    = models.DateField(null=True)

    desconto_indicacoes = models.DecimalField("Desconto por Indicações:", max_digits=5, decimal_places=2, default=0, null=True,blank=True)
    cadastrado_por = models.ForeignKey(entidade,  related_name = "cadastrado_por",default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name = "alterado_por",default=1)
    ativo = models.BooleanField(default=True)

    def serialize(self):
        serialized_values = {}

class Indicacao (models.Model):
    cliente = models.ForeignKey(entidade, related_name = "cliente")
    indicacao = models.ForeignKey(entidade,related_name = "indicacao")
    taxa_desconto = models.DecimalField("Taxa Desconto",max_digits=5, decimal_places=2, default=0)
    indicacao_ativa = models.BooleanField(default=True)
    cadastrado_por = models.ForeignKey(entidade, related_name="indicacao_cadastrado_por", default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name="indicacao_alterado_por", default=1)
