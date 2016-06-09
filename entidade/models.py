# -*- encoding: utf-8 -*-
from django.db import models
from rest_framework import serializers


MENSAGENS_ERROS={'required': 'Campo Obrigatório!',
                 'invalid' : 'Formato Inválido!'
                }


class natureza_juridica(models.Model):    
    codigo_natureza   = models.CharField("Código:",max_length=5,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    natureza_juridica = models.CharField("Natureza Jurídica:",max_length=100,null=False,unique=True,error_messages=MENSAGENS_ERROS)

class observacao(models.Model):
    
    data      = models.DateField("Data:",null=False,auto_now=True)
    #autor     = models.ForeignKey()
    
    descricao = models.TextField("Descrição: ",max_length=500,null=False,error_messages=MENSAGENS_ERROS)
    
class localizacao_simples(models.Model):
    cep         = models.CharField("Codigo Postal:",max_length=8,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    logradouro  = models.CharField("Logradouro:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    numero      = models.CharField("Numero:",max_length=5,null=True,error_messages=MENSAGENS_ERROS)
    complemento = models.CharField("Complemento:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)    
    #codigo_ibge = models.CharField("Codigo IBGE:",max_length=10,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    bairro           = models.CharField("Bairro:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    codigo_ibge = models.CharField("Codigo Municipal:",max_length=7,null=False,error_messages=MENSAGENS_ERROS)
    municipio        = models.CharField("Municipio:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    #sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    estado        = models.CharField("Estado:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)    
    
    
    pais        = models.CharField("País:",max_length=30,null=False,error_messages=MENSAGENS_ERROS)
    #sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    
    def get_endereco(self):
        return self.logradouro+","+self.numero+","+self.bairro+","+self.municipio+","+self.estado+" - "+self.cep    
    
class entidade(models.Model):
    opcoes_tipos_registros = (
                            
        ('C', 'CLIENTE'),
        ('F', 'FORNECEDOR'),
        ('U', 'FUNCIONARIO'),
        ('O', 'OUTRO'),
    )
    
    cpf_cnpj              = models.CharField("Cpf / Cnpj:",max_length=18,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    
    nome_razao            = models.CharField("Nome / Razão Social:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS) 
    apelido_fantasia      = models.CharField("Apelido / Nome Fantasia:",max_length=50,null=True,blank=True,unique=False,error_messages=MENSAGENS_ERROS)
    
    registro_geral        = models.CharField("Identidade:",max_length=12,null=True,unique=False,blank=True,error_messages=MENSAGENS_ERROS)
    tipo_registro         = models.CharField("Tipo Registro:",max_length=1,null=True,default='C',unique=False,error_messages=MENSAGENS_ERROS)
    inscricao_estadual    = models.CharField("Inscrição Estadual:",max_length=10,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    inscricao_municipal   = models.CharField("Inscrição Municipal:",max_length=10,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    inscricao_rural       = models.CharField("Inscrição Rural:",max_length=10,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    
    nascimento_fundacao   = models.DateField("Nascimento / Fundação:",null=True,blank=True)
    
    data_cadastro         = models.DateField(auto_now=True)
    ativo          = models.BooleanField(default=True)
    
    numeracao_protocolo = models.IntegerField(null=False,default=1)
    
    endereco = models.ForeignKey(localizacao_simples,default=0)
    

    def __unicode__(self):
        return unicode(self.nome_razao)
    
#class indicacao(models.Model):
#    data = models.DateField(null=False,auto_now=False, input_formats=['%d/%m/%Y'],error_messages=MENSAGENS_ERROS)

class contato(models.Model):
    opcoes_tipos_contatos = (
                            
        ('C', 'CELULAR'),
        ('F', 'COMERCIAL'),
        ('R', 'RESIDENCIAL'),
        ('O', 'OUTROS'),
    )
    
    entidade = models.ForeignKey(entidade)
    tipo_contato         = models.CharField("Tipo:",max_length=1,null=False,choices=opcoes_tipos_contatos, default='C',error_messages=MENSAGENS_ERROS)
    numero = models.CharField("Numero:",max_length=20,null=False,blank=True,error_messages=MENSAGENS_ERROS)
    nome_contato = models.CharField("Nome do Contato:",max_length=50,null=False,blank=True,error_messages=MENSAGENS_ERROS)
    cargo_setor = models.CharField("Cargo ou Setor:",max_length=50,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    email = models.EmailField(max_length=100,null=True,blank=True,error_messages=MENSAGENS_ERROS)



class Pais(models.Model):
    nome        = models.CharField("País:",max_length=100,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
    
    def __unicode__(self):
        return unicode(self.nome) 

class Estado(models.Model):
    codigo_ibge = models.CharField("Codigo IBGE:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    sigla       = models.CharField("Sigla:",max_length=2,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Estado:",max_length=100,null=False,unique=True,error_messages=MENSAGENS_ERROS)    
    regiao      = models.CharField("Região:",max_length=20,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    pais        = models.ForeignKey(Pais)
    
    def __unicode__(self):
        return unicode(self.nome) 
    
class Municipio(models.Model):
    codigo_ibge = models.CharField("Codigo Municipal:",max_length=7,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Municipio:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    estado      = models.ForeignKey(Estado)  
    
    def __unicode__(self):
        return unicode(self.nome) 

class Bairro(models.Model):
    codigo_ibge = models.CharField("Codigo IBGE:",max_length=10,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome           = models.CharField("Bairro:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    municipio      = models.ForeignKey(Municipio)
    
    class Meta:
        unique_together = ('nome', 'municipio')
        
    def __unicode__(self):
        return unicode(self.nome)   
        
class Logradouro(models.Model):
    cep         = models.CharField("Codigo Postal:",max_length=8,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Endereço:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    bairro      = models.ForeignKey(Bairro)
    
    def __unicode__(self):
        return unicode(self.nome) 

class Localizacao(models.Model):
    logradouro  = models.ForeignKey(Logradouro)
    numero      = models.CharField("Numero:",max_length=5,null=True,unique=False,error_messages=MENSAGENS_ERROS)
    complemento = models.CharField("Complemento:",max_length=100,null=True,unique=False,error_messages=MENSAGENS_ERROS)
    
class Endereco(object):
    
    logradouro   = None
    bairro       = None
    municipio    = None
    estado       = None
    pais         = None
    codigo_bairro = None
    codigo_municipio = None   
    
class endereco_serializer(serializers.Serializer):
    
    logradouro   = serializers.CharField(max_length=100)
    bairro       = serializers.CharField(max_length=100)
    municipio    = serializers.CharField(max_length=100)
    estado       = serializers.CharField(max_length=100)
    pais         = serializers.CharField(max_length=100)
    codigo_municipio = serializers.CharField(max_length=7)
    codigo_bairro = serializers.CharField(max_length=10)