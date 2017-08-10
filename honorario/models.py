# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from entidade.formularios import MENSAGENS_ERROS
from entidade.models import entidade
from django.db import models


class Contrato(models.Model):
    opcoes_tipos_clientes = (('PF', 'PESSOA FISICA'), ('PJ', 'PESSOA JURIDICA'),)
    tipo_cliente  = models.CharField("Tipo do Cliente:",max_length=2,null=False,default='PJ',choices = opcoes_tipos_clientes,error_messages=MENSAGENS_ERROS)

    vigencia_inicio = models.DateField(null=False)
    vigencia_fim    = models.DateField(null=False)

    tipo_contrato = models.ForeignKey(entidade,default=0)

    taxa_honorario  = models.DecimalField("Honorário:", max_digits=5, decimal_places=2, null=False,blank=False)
    valor_honorario = models.DecimalField("Valor:", max_digits=6, decimal_places=2, null=False,blank=False)
    dia_vencimento  = models.IntegerField("Dia do Vencimento:",null=False,default=5)

    desconto_temporario = models.DecimalField("Desconto Temporário:", max_digits=5, decimal_places=2, null=True,blank=True)
    desconto_inicio = models.DateField(null=True)
    desconto_fim    = models.DateField(null=True)

    desconto_indicacoes = models.DecimalField("Desconto por Indicações:", max_digits=5, decimal_places=2, null=True,blank=True)
    cadastrado_por = models.ForeignKey(entidade,  related_name = "cadastrado_por",default=0)
    data_cadastro = models.DateField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name = "alterado_por",default=0)
    ativo = models.BooleanField(default=True)

    def serialize(self):
        serialized_values = {}