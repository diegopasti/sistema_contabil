# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from entidade.models import entidade


MENSAGENS_ERROS={'required': 'Campo Obrigatório!',
                 'invalid' : 'Formato Inválido!'
                }

class pais(models.Model):
    nome        = models.CharField("Estado:",max_length=100,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)

class estado(models.Model):
    codigo_ibge = models.CharField("Código IBGE:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Estado:",max_length=100,null=False,unique=True,error_messages=MENSAGENS_ERROS)    
    regiao      = models.CharField("Região:",max_length=20,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    pais        = models.ForeignKey(pais)
    
class municipio(models.Model):
    codigo_ibge = models.CharField("Código Municipal:",max_length=7,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Município:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    estado      = models.ForeignKey(estado)  

class bairro(models.Model):
    codigo_ibge = models.CharField("Código IBGE:",max_length=10,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome           = models.CharField("Bairro:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    municipio      = models.ForeignKey(municipio)
    
    class Meta:
        unique_together = ('nome', 'municipio')
        
    def __unicode__(self):
        return unicode(self.nome)    
    
        
class endereco(models.Model):
    cep         = models.CharField("Código Postal:",max_length=8,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Endereço:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    bairro      = models.ForeignKey(bairro)
    
    def __unicode__(self):
        return unicode(self.nome)    
    
class localizacao(models.Model):
    entidade     = models.ForeignKey(entidade)
    cep          = models.ForeignKey(endereco)
    numero       = models.CharField("Numero:",max_length=5,null=False,error_messages=MENSAGENS_ERROS)
    complemento  = models.CharField("Complemento:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    
    class Meta:
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

