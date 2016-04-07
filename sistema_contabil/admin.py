'''
Created on 2 de dez de 2015

@author: Diego
'''

from django.contrib import admin
from endereco.models import entidade, endereco, bairro #,localizacao
from entidade.models import contato #, endereco, bairro #,localizacao
from entidade.protocolo.models import protocolo, item_protocolo
    
    
class entidade_admin(admin.ModelAdmin):
    list_display = ('cpf_cnpj','tipo_registro','nome_razao', 'apelido_fantasia','data_cadastro','ativo')
    
class endereco_admin(admin.ModelAdmin):
    list_display = ('cep','nome','bairro',)
    
class contato_admin(admin.ModelAdmin):
    list_display = ('entidade','tipo_contato','numero','nome_contato','cargo_setor','email')

class localizacao_admin(admin.ModelAdmin):
    list_display = ('entidade','cep','numero','complemento','bairro')
    
    def bairro(self,obj):
        end = endereco.objects.get(pk=obj.cep_id)
        return bairro.objects.get(pk=end.bairro_id)
        

admin.site.register(entidade,entidade_admin)
admin.site.register(contato,contato_admin)
admin.site.register(endereco,endereco_admin)
#admin.site.register(localizacao,localizacao_admin)
admin.site.register(protocolo)
admin.site.register(item_protocolo)


