# -*- encoding: utf-8 -*-
from django.db import models

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
    

class entidade(models.Model):
    opcoes_tipos_registros = (
                            
        ('C', 'CLIENTE'),
        ('F', 'FORNECEDOR'),
        ('U', 'FUNCIONARIO'),
        ('O', 'OUTRO'),
    )
    
    cpf_cnpj              = models.CharField("Cpf / Cnpj:",max_length=18,null=False,unique=True,error_messages=MENSAGENS_ERROS)
    registro_geral        = models.CharField("Identidade:",max_length=12,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    tipo_registro         = models.CharField("Tipo Registro:",max_length=1,null=False,choices=opcoes_tipos_registros, default='C',error_messages=MENSAGENS_ERROS)
    nome_razao            = models.CharField("Nome / Razão Social:",max_length=100,null=False,unique=False,error_messages=MENSAGENS_ERROS) 
    apelido_fantasia      = models.CharField("Apelido / Nome Fantasia:",max_length=50,null=False,unique=False,error_messages=MENSAGENS_ERROS)
    inscricao_estadual    = models.BooleanField("Inscrição Estadual:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    inscricao_municipal   = models.BooleanField("Inscrição Municipal:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    inscricao_rural       = models.BooleanField("Inscrição Rural:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    
    nascimento_fundacao   = models.DateField("Nascimento / Fundação:",null=True)
    
    data_cadastro         = models.DateField(auto_now=True)
    ativo          = models.BooleanField(default=True)
    
    numeracao_protocolo = models.IntegerField(null=False,default=0)
    

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
    numero       = models.CharField("Número:",max_length=5,null=False,error_messages=MENSAGENS_ERROS)
    complemento  = models.CharField("Complemento:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    
    class Meta:
        verbose_name = "Localizacao"
        verbose_name_plural = "Localizações"

class protocolo(models.Model):
    emissor      = models.ForeignKey(entidade,related_name='entidade_emissora')
    destinatario = models.ForeignKey(entidade,related_name='entidade_destinataria')
    data_emissao = models.DateField(auto_now=True)
    
    numeracao_destinatario = models.IntegerField(null=True)
    
class item_protocolo(models.Model):    
    protocolo      = models.ForeignKey(protocolo)
    documento      = models.CharField("Item:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    referencia     = models.DateField("Mês de Referência:",null=True,error_messages=MENSAGENS_ERROS)
    vencimento     = models.DateField("Vencimento:",null=True,error_messages=MENSAGENS_ERROS)
    valor          = models.DateField("Valor:",null=True,error_messages=MENSAGENS_ERROS)
    complemento    = models.TextField("Descrição:",max_length=500,null=True,error_messages=MENSAGENS_ERROS)






    



    