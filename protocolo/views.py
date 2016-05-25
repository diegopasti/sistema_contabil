# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''

from decimal import Decimal
import os

from django.conf.global_settings import STATIC_URL
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from entidade.formularios import formulario_emitir_protocolo, formulario_confirmar_entrega
from entidade.models import entidade, contato  # , localizacao
from entidade.views import verificar_erros_formulario, formatar_cpfcnpj, construir_endereco
from protocolo.models import protocolo, item_protocolo
from sistema_contabil.settings import BASE_DIR


#from sistema_contabil.settings import BASE_DIR, STATIC_URL
#from endereco.models import localizacao
def cadastro_protocolo(request):
    
    erro = False
    if (request.method == "POST"):
        print "Temos que terminar a funcionalidade de dar baixa"
        form_entrega = formulario_confirmar_entrega(request.POST)
        
        if form_entrega.is_valid(): 
            print "Parece que deu tudo certo.."
            
        else:
            print "tem algum erro no formulario.."
            msg = verificar_erros_formulario(form_entrega)
            messages.add_message(request, messages.SUCCESS, msg)
            erro = True
            
    else:
        form_entrega = formulario_confirmar_entrega()
    dados = protocolo.objects.all()
    return render_to_response("protocolo/cadastro_protocolo.html",{"form_entrega":form_entrega,'dados':dados,'erro':erro},context_instance=RequestContext(request))

"""
def imprimir_protocolo(request,emissor,destinatario,documentos,):
    from django.template import Context
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens")
"""

def gerar_pdf(request,formulario):
    from django.template import Context# loader,Context, Template
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens\\")
    emissor = entidade.objects.get(pk=1)
    
    destinatario = formulario['entidade_destinatario'].value()
    
    if '|' in destinatario:
        campos = destinatario.split("|")
        destinatario_nome = campos[0]
        destinatario_cpf_cnpj = formatar_cpf_cnpj(campos[1])
        destinatario_complemento = ""
        codigo_protocolo = "AVULSO"
        
        print campos[2].title()
        destinatario_endereco = campos[2].title()
        
        if campos[3] == "":
            destinatario_contatos = []
        else:
            destinatario_contatos = [campos[3]]
    
    else:
        destinatario = destinatario[:destinatario.find(" - ")]
        destinatario = int(destinatario)
        destinatario = entidade.objects.get(pk=destinatario)
        
        destinatario_nome = destinatario.nome_razao.upper()
        destinatario_cpf_cnpj = formatar_cpf_cnpj(destinatario.cpf_cnpj)
        
        codigo_protocolo = "%05d"%(destinatario.numeracao_protocolo)
        destinatario_endereco = destinatario.endereco
        destinatario_endereco = "%s, %s, %s, %s, %s - %s"%(destinatario_endereco.logradouro,destinatario_endereco.numero,destinatario_endereco.bairro,destinatario_endereco.municipio, destinatario_endereco.estado, formatar_cep(destinatario_endereco.cep))
        destinatario_endereco = destinatario_endereco.title()
        
        print destinatario_endereco
        
        destinatario_complemento = destinatario.endereco.complemento.title()
        destinatario_contatos = []
        
        for item in contato.objects.filter(entidade=destinatario):
            destinatario_contatos.append(item.numero)
    
    
    recebido_por = 'DIEGO PASTI'
    identidade = "128.598.557-50"
    data_entrega = '12/04/2015'
    hora_entrega = '14:25'
    print "olha o que temos nos documentos: ",formulario.temporarios
    parametros = {
                  'emissor_cpf_cnpj':formatar_cpf_cnpj(emissor.cpf_cnpj),
                  'emissor_endereco':"Reta da Penha, Vitoria - ES",
                  
                  'destinatario_nome':destinatario_nome,
                  'destinatario_cpf_cnpj':destinatario_cpf_cnpj,
                  'destinatario_endereco':destinatario_endereco,
                  'destinatario_complemento':destinatario_complemento,
                  #destinatario.endereco_id.complemento
                  
                  'destinatario_contatos':destinatario_contatos,
    
                  
                  'codigo_protocolo':codigo_protocolo,
                  'emitido_por':'Marcelo',
                  
                  'recebido_por':recebido_por,
                  'identificacao':identidade,
                  'data_entrega':data_entrega,
                  'hora_entrega':hora_entrega,
                  
                  
                  
                  #'emissor':emissor,
                  
                  #'destinatario':destinatario,
                  #'endereco_destinatario':endereco,
                  #'contatos_destinatario':contatos,
                  
                  
                  
                  'documentos':formulario.temporarios,
                  #'documentos':[
                  #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                  #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                  #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                  #              ],
                  'formulario_protocolo':"Nada por enquanto",
                  'erro':"sem erros tambem",
                  'path':path,
                  
                  'path_imagens':path
                   
                }
    
    c = Context(parametros)#{'message': 'Your message'})
    
    # RENDERIZAR NORMAL
    #return render_to_response('protocolo/imprimir_protocolo.html', c)
    
    # RENDERIZAR PDF
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp,context=c)
    return result

def emitir_protocolo(request,numero_item):
    numero_item = int(numero_item)
    erro = False
    destinatarios = entidade.objects.all()[1:]  
    
    if (request.method == "POST"):
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST)
        #print "olha o request:",formulario_protocolo
            
        #print "O que que tem nos temporarios: ",formulario_protocolo.temporarios
        
        if 'adicionar_item' in request.POST:
            
            if formulario_protocolo.is_valid(): 
                item            = item_protocolo()
                item.documento  = formulario_protocolo['documento'].value().upper()
                item.complemento= formulario_protocolo['complemento'].value().upper()
                item.referencia = formulario_protocolo['referencia'].value()
                item.vencimento = formulario_protocolo['vencimento'].value()
                
                valor = formulario_protocolo['valor'].value()
                
                if valor != "":
                    valor = valor.replace(".","")
                    valor = valor.replace(",",".")
                    item.valor      = Decimal(valor)
                
                formulario_protocolo.temporarios.append(item)
                
                cliente = formulario_protocolo['entidade_destinatario'].value().upper()
                temp = formulario_protocolo.temporarios
                
                formulario_protocolo  = formulario_emitir_protocolo({'entidade_destinatario':cliente})
                formulario_protocolo.temporarios = temp
                
                #messages.add_message(request, messages.SUCCESS, "Item adicionado com sucesso")
            
            else:
                msg = verificar_erros_formulario(formulario_protocolo)
                messages.add_message(request, messages.SUCCESS, msg)
                erro = True
            
            
        elif 'gerar_protocolo' in request.POST:
            
            """
                TENHO QUE VERIFICAR UM JEITO DE ABRIR O PDF EM UMA OUTRA ABA, E RESETAR A ATUAL, OU RESETAR A ATUAL
                NO CASO DELE VOLTAR PRA PAGINA..
            """
            backup_request = request
            backup_formulario = formulario_protocolo
            
            formulario_protocolo = formulario_emitir_protocolo()
            formulario_protocolo.limpar_temporarios()
            
            resposta_pdf = gerar_pdf(backup_request,backup_formulario)
            return resposta_pdf 
        
        elif 'excluir_item' in request.POST:
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            #print formulario_protocolo["excluir_item"]
            
            try:
                formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[int(formulario_protocolo["excluir_item"].value())])
            except:
                pass
            
            """
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            #print "O que que tem nos temporarios: ",formulario_protocolo.temporarios
            formulario_protocolo.temporarios = formulario_protocolo.temporarios
            nome_cliente = formulario_protocolo['entidade_destinatario'].value().upper()
            id_cliente = int(nome_cliente[:nome_cliente.index("-")])
            cliente = entidade.objects.get(pk=id_cliente)
            #cliente.cpf_cnpj = formatar_cpfcnpj(cliente.cpf_cnpj)
            
            
            try:
                empresa = entidade.objects.get(pk=1)
            except:
                print "Nao temos um registro da emrpesa ainda.. vamos usar o default"
                
            print "Tem algum registro da empresa:",empresa
            empresa.cpf_cnpj = formatar_cpfcnpj(empresa.cpf_cnpj)
            endereco_cliente = construir_endereco(localizacao.objects.get(entidade_id=cliente.id))
            endereco_emissor = construir_endereco(localizacao.objects.get(entidade_id=empresa.id))
            
            
            
            p = protocolo()
            p.emissor = empresa
            p.destinatario = cliente
            p.numeracao_destinatario = cliente.numeracao_protocolo
            p.save()
            print "Salvei o protocolo?"
            
            cliente.numeracao_protocolo = cliente.numeracao_protocolo + 1
            cliente.save()
            print "Incrementei o contador do protocolo do cliente"
                
            salvar_itens_protocolos(protocolo,formulario_protocolo.temporarios)
            
            
            formulario_protocolo = formulario_emitir_protocolo()
            formulario_protocolo.limpar_temporarios()
            
            parametros = {'emissor':empresa,
                          'destinatario':cliente,
                          'endereco_destinatario':endereco_cliente,
                          'endereco_emissor':endereco_emissor,
                          'documentos':formulario_protocolo.temporarios,
                          'formulario_protocolo':formulario_protocolo,
                          'erro':erro}
            
            
            from django.template import loader,Context, Template
            from xhtml2pdf import pisa
           
            c = Context(parametros)#{'message': 'Your message'})
            from django_xhtml2pdf.utils import generate_pdf
            resp = HttpResponse(content_type='application/pdf')
            result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp,context=c)
            
            return result
        
        """
            
    else:
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_protocolo.limpar_temporarios()
        
        """
        if "excluir" in request.path:
            print "Acho que estou tentando apagar algum item"
            formulario_protocolo = formulario_emitir_protocolo(request.GET)
            print "olha os temporarios: ",formulario_protocolo.temporarios
            
            temp = formulario_protocolo.temporarios
            cliente = formulario_protocolo.destinatario_temporario
                
            formulario_protocolo  = formulario_emitir_protocolo({'entidade_destinatario':cliente})
            formulario_protocolo.destinatario_temporario = cliente
            
            print "olha o destinatario: ",formulario_protocolo['entidade_destinatario'].value().upper()
            formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[numero_item])
            print "olha os temporarios depois: ",formulario_protocolo.temporarios
            
            return render_to_response("emitir_protocolo.html",{'destinatarios':destinatarios ,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro},context_instance=RequestContext(request))
            
        #else:
        """ 
        
                    
    return render_to_response("protocolo/emitir_protocolo.html",{'destinatarios':destinatarios ,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro},context_instance=RequestContext(request))


def salvar_itens_protocolos(protocolo,itens_protocolo):
    for item in itens_protocolo:                
        item.protocolo = protocolo
        item.save()
        
        
        
        
        
        
"""
 
 COISAS QUE PODEM SER COLOCADAS EM OUTROS LUGARES

"""

def formatar_cep(cep):
    cep_formatado = ""+cep[:2]+"."+cep[2:5]+"-"+cep[5:]
    return cep_formatado

def formatar_cpf_cnpj(codigo):
    if len(codigo) == 11:
        codigo_formatado = codigo[:3]+"."+codigo[3:6]+"."+codigo[6:9]+"-"+codigo[9:]
    else:
        codigo_formatado = codigo[:2]+"."+codigo[2:5]+"."+codigo[5:8]+"/"+codigo[9:12]+"-"+codigo[12:]
    return codigo_formatado

