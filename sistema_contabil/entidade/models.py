# -*- encoding: utf-8 -*-
from django.db import models



MENSAGENS_ERROS={'required': 'Campo Obrigatório!',
                 'invalid' : 'Formato Inválido!'
                }




class entidade(models.Model):
    opcoes_tipos_registros = (
                            
        ('C', 'Cliente'),
        ('F', 'Fornecedor'),
        ('U', 'Funcionário'),
        ('O', 'Outro'),
    )
    
    cpf_cnpj              = models.CharField("Cpf / Cnpj:",max_length=18,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    registro_geral        = models.CharField("Identidade:",max_length=12,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    tipo_registro         = models.CharField("Tipo Registro:",max_length=1,null=False,choices=opcoes_tipos_registros, default='C',error_messages=MENSAGENS_ERROS)
    nome_razao            = models.CharField("Nome / Razão Social:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS) 
    apelido_fantasia         = models.CharField("Apelido / Nome Fantasia:",max_length=50,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    inscricao_estadual    = models.BooleanField("Inscrição Estadual:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    inscricao_municipal   = models.BooleanField("Inscrição Municipal:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    inscricao_rural       = models.BooleanField("Inscrição Rural:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    
    nascimento_fundacao   = models.DateField("Nascimento / Fundação:",null=True)
    
    data_cadastro         = models.DateField(auto_now=True)
    desabilitado          = models.BooleanField(default=False)
#class indicacao(models.Model):
#    data = models.DateField(null=False,auto_now=False, input_formats=['%d/%m/%Y'],error_messages=MENSAGENS_ERROS)

class contato(models.Model):
    opcoes_tipos_contatos = (
                            
        ('C', 'Celular'),
        ('F', 'Comercial'),
        ('R', 'Residencial'),
        ('O', 'Outros'),
    )
    
    entidade = models.ForeignKey(entidade)
    tipo_contato         = models.CharField("Tipo:",max_length=1,null=False,choices=opcoes_tipos_contatos, default='C',error_messages=MENSAGENS_ERROS)
    numero = models.CharField("Numero:",max_length=20,null=False,error_messages=MENSAGENS_ERROS)
    nome_contato = models.CharField("Nome do Contato:",max_length=50,null=False,error_messages=MENSAGENS_ERROS)
    cargo_setor = models.CharField("Cargo ou Setor:",max_length=50,null=True,error_messages=MENSAGENS_ERROS)
    email = models.EmailField(max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    


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
    codigo_ibge = models.CharField("Código Municípal:",max_length=7,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Município:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    estado      = models.ForeignKey(estado)  

class bairro(models.Model):
    codigo_ibge = models.CharField("Código IBGE:",max_length=10,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome           = models.CharField("Bairro:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    municipio      = models.ForeignKey(municipio)
    
    class Meta:
        unique_together = ('nome', 'municipio')
        
class endereco(models.Model):
    cep         = models.CharField("Código Postal:",max_length=8,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    nome        = models.CharField("Endereço:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    bairro      = models.ForeignKey(bairro)
    
class localizacao(models.Model):
    cep          = models.ForeignKey(endereco)
    numero       = models.CharField("Número:",max_length=5,null=False,error_messages=MENSAGENS_ERROS)
    complemento  = models.CharField("Complemento:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    