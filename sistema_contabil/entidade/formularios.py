# -*- encoding: utf-8 -*-
'''
Created on 2 de set de 2015

@author: Diego
'''

from django import forms


MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
                }

class formulario_cadastro_entidade_completo(forms.Form):
    opcoes_tipos_registros = (
                            
        ('C', 'CLIENTE'),
        ('F', 'FORNECEDOR'),
        ('U', 'FUNCIONÁRIO'),
        ('O', 'OUTRO'),
    )
    
    cpf_cnpj              = forms.CharField(label="Cpf / Cnpj:",max_length=18,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control", 'id':'cpf_cnpj' }),
                                            )
    nome_razao            = forms.CharField(label="Nome / Razão Social:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control", 'id':'nome_razao'})
                                            ) 
    
    apelido_fantasia      = forms.CharField(label="Apelido / Nome Fantasia:",max_length=50,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'apelido_fantasia'})
                                            )
    tipo_registro         = forms.ChoiceField(label="Tipo Registro:",choices=opcoes_tipos_registros,required=True,error_messages=MENSAGENS_ERROS, #choices=opcoes_tipos_registros, default='C',
                                            widget=forms.Select(attrs={'class':"form-control" ,'id':'tipo_registro'})
                                            )
    
    registro_geral        = forms.CharField(label="Inscrição Estadual / Identidade:",max_length=12,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'registro_geral'})
                                            )
    
    nascimento_fundacao   = forms.DateField(label="Nascimento / Fundação:",required=False,
                                            widget= forms.DateInput(attrs={'class':"form-control" ,'id':'nascimento_fundacao'},format = '%d/%m/%Y'), 
                                            input_formats=('%d/%m/%Y',)
                                            )
    
    cep          = forms.CharField(label="Código Postal:",max_length=15,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_postal'})
                                            )
                                   
    numero_endereco       = forms.CharField(label="Número:",max_length=5,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_endereco'})
                                            )
    complemento  = forms.CharField(label="Complemento:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'complemento'})
                                            )
    
    endereco    = forms.CharField(label="Endereço:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control" ,'id':'endereco'})
                                  )
    bairro      = forms.CharField(label="Bairro:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control" ,'id':'bairro'})
                                  )
    
    codigo_municipio = forms.CharField(label="Código Município:",max_length=10,required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_municipio'})
                                  )
    municipio = forms.CharField(label="Município:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control" ,'id':'municipio'})
                                  )
    
    opcoes_estados = (
                            
        ('AC', 'ACRE'),
        ('AL', 'ALAGOAS'),
        ('AM', 'AMAZONAS'),
        ('AP', 'AMAPÁ'),
        ('BA', 'BAHIA'),
        ('CE', 'CEARÁ'),
        ('DF', 'DESTRITO FEDERAL'),
        ('ES', 'ESPIRÍTO SANTO'),
        ('GO', 'GOIÁS'),
        ('MA', 'MARANHÃO'),
        ('MG', 'MINAS GERAIS'),
        ('MS', 'MATO GROSSO DO SUL'),
        ('MT', 'MATO GROSSO'),
        ('PA', 'PARÁ'),
        ('PB', 'PARAÍBA'),
        ('PE', 'PERNAMBUCO'),
        ('PI', 'PIAUÍ'),
        ('PR', 'PARANÁ'),
        ('RJ', 'RIO DE JANEIRO'),
        
        ('RN', 'RIO GRANDE DO NORTE'),
        ('RO', 'RONDÔNIA'),
        ('RR', 'RORAIMA'),
        ('RS', 'RIO GRANDE DO SUL'),
        ('SC', 'SANTA CATARINA'),
        ('SE', 'SERGIPE'),
        ('SP', 'SÃO PAULO'),
        ('TO', 'TOCANTIS'),
        
    )
    
    estado       = forms.ChoiceField(label="Estado:",choices=opcoes_estados,required=True,error_messages=MENSAGENS_ERROS,
                                         widget=forms.Select(attrs={'class':"form-control" ,'id':'estado'})
                                  )

    pais       = forms.CharField(label="País:",required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control" ,'id':'pais'})
                                  )
    
    opcoes_tipos_contatos = (
                            
        ('C', 'CELULAR'),
        ('F', 'COMERCIAL'),
        ('R', 'RESIDENCIAL'),
        ('O', 'OUTROS'),
    )
    
    tipo_contato  = forms.ChoiceField(label="Tipo:",choices=opcoes_tipos_contatos,required=True,error_messages=MENSAGENS_ERROS, # choices=opcoes_tipos_contatos,default='C',)
                                    widget=forms.Select(attrs={'class':"form-control" ,'id':'tipo_contato'})
                                    )
    
    numero_contato        = forms.CharField(label="Telefone:",max_length=15,required=True,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_contato'})
                                    )
    cargo_setor   = forms.CharField(label="Cargo ou Setor:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'cargo_setor'})
                                    )
    email         = forms.EmailField(max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                     widget=forms.TextInput(attrs={'class':"form-control" ,'id':'email:'})
                                    )
    
    #inscricao_estadual    = forms.BooleanField("Inscrição Estadual:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_municipal   = forms.BooleanField("Inscrição Municipal:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_rural       = forms.BooleanField("Inscrição Rural:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #data_cadastro         = forms.DateField(auto_now=True)
    #desabilitado          = forms.BooleanField(default=False)    

    #entidade = forms.ForeignKey(entidade)
