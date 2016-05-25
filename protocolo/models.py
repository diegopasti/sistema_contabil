# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''
from django.db import models

from entidade.models import entidade
from entidade.formularios import MENSAGENS_ERROS

class protocolo(models.Model):
    emissor      = models.ForeignKey(entidade,related_name='entidade_emissora')
    destinatario = models.ForeignKey(entidade,related_name='entidade_destinataria')
    data_emissao = models.DateField(auto_now=True)
    numeracao_destinatario = models.IntegerField(null=True)
    
    data_recebimento = models.DateField(null=True)
    recebido_por     = models.CharField("Recebido por:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    doc_receptor     = models.CharField("Identidade:",max_length=20,null=True,error_messages=MENSAGENS_ERROS)
    situacao         = models.BooleanField(default=False)
     
    
class item_protocolo(models.Model):    
    protocolo      = models.ForeignKey(protocolo)
    documento      = models.CharField("Item:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    referencia     = models.CharField("Mês de Referência:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    vencimento     = models.CharField("Vencimento:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    valor          = models.CharField("Valor:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    complemento    = models.TextField("Complemento:",max_length=500,null=True,error_messages=MENSAGENS_ERROS)
