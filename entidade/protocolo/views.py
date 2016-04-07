# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''

from decimal import Decimal
import os

from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from entidade.formularios import formulario_emitir_protocolo, \
    formulario_confirmar_entrega
from entidade.models import entidade#, localizacao
from endereco.models import localizacao
from entidade.protocolo.models import protocolo, item_protocolo
from entidade.views import verificar_erros_formulario, formatar_cpfcnpj, construir_endereco
from sistema_contabil.settings import BASE_DIR


def cadastro_protocolo(request):
        
    if (request.method == "POST"):
        pass
    else:
        form_entrega = formulario_confirmar_entrega()
    dados = protocolo.objects.all()
    return render_to_response("protocolo/cadastro_protocolo.html",{"form_entrega":form_entrega,'dados':dados,'erro':False},context_instance=RequestContext(request))

def gerar_pdf(request):
    from django.template import loader,Context, Template
    from xhtml2pdf import pisa
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens")
   
    parametros = {'emissor':"Digitar Contabilidade",
                  'emitido_por':'Marcelo',
                  'destinatario':"HELDER PASTI",
                  'endereco_destinatario':"Rua demosthenes Nunes Vieira, 60, Alto Lage, Cariacica - ES",
                  'endereco_emissor':"Reta da Penha, Vitoria - ES",
                  'codigo_protocolo':"00012",
                  'documentos':[
                                    ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                                    ["8","EMISSÃO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                                    ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                                ],
                  'formulario_protocolo':"Nada por enquanto",
                   'erro':"sem erros tambem",
                   'path':path
                }
    
    
    
    c = Context(parametros)#{'message': 'Your message'})
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp,context=c)
    return result

def emitir_protocolo(request,numero_item):
    numero_item = int(numero_item)
    erro = False
    destinatarios = entidade.objects.all()  
    
    if (request.method == "POST"):
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST)
            
        print "O que que tem nos temporarios: ",formulario_protocolo.temporarios
        
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
            
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            #print "O que que tem nos temporarios: ",formulario_protocolo.temporarios
                        
            formulario_protocolo.temporarios = formulario_protocolo.temporarios
            
            
                
            
            nome_cliente = formulario_protocolo['entidade_destinatario'].value().upper()
            id_cliente = int(nome_cliente[:nome_cliente.index("-")])
            
            cliente = entidade.objects.get(pk=id_cliente)
            cliente.cpf_cnpj = formatar_cpfcnpj(cliente.cpf_cnpj)
            
            empresa = entidade.objects.get(pk=1)
            empresa.cpf_cnpj = formatar_cpfcnpj(empresa.cpf_cnpj)
            
            endereco_cliente = construir_endereco(localizacao.objects.get(entidade_id=cliente.id))
            endereco_emissor = construir_endereco(localizacao.objects.get(entidade_id=empresa.id))
            
            p = protocolo()
            
            print "OLHA O CLIENTE: ",
            p.emissor = empresa
            p.destinatario = cliente
            p.numeracao_destinatario = cliente.numeracao_protocolo
            p.save()
            print "Salvei o protocolo?"
            
            cliente.numeracao_protocolo = cliente.numeracao_protocolo + 1
            cliente.save()
            print "Incrementei o contador do protocolo do cliente"
            
            for item in formulario_protocolo.temporarios:                
                item.protocolo = p
                print item.protocolo     
                print item.documento     
                print item.referencia    
                print item.vencimento    
                print item.valor         
                print item.complemento
                item.save()
            
            print "Consegui?"
            
            formulario_protocolo = formulario_emitir_protocolo()
            formulario_protocolo.limpar_temporarios()
            
            """
            data_emissao = models.DateField(auto_now=True)
            numeracao_destinatario = models.IntegerField(null=True)
            
            data_recebimento = models.DateField(null=True)
            recebido_por     = models.CharField("Recebido por:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
            doc_receptor     = models.CharField("Identidade:",max_length=20,null=True,error_messages=MENSAGENS_ERROS)
            situacao
            """ 
            
            pagina = "protocolo.html"
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
            
            
        elif 'excluir_item' in request.POST:
            #print "Axo que eh um POST pra apagar"
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            print formulario_protocolo["excluir_item"]
            formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[int(formulario_protocolo["excluir_item"].value())])
            
            
        
            
    else:
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_protocolo.limpar_temporarios()
        """
        if "excluir" in request.path:
            formulario_protocolo = formulario_emitir_protocolo(request.GET)
            print "olha os temporarios: ",formulario_protocolo.temporarios
            
            
            temp = formulario_protocolo.temporarios
            cliente = formulario_protocolo.destinatario_temporario
                
            formulario_protocolo  = formulario_emitir_protocolo({'entidade_destinatario':cliente})
            formulario_protocolo.destinatario_temporario = cliente
            formulario_protocolo.temporarios = temp
            
            
            print "olha o destinatario: ",formulario_protocolo['entidade_destinatario'].value().upper()
            formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[numero_item])
            print "olha os temporarios depois: ",formulario_protocolo.temporarios
            
            return render_to_response("emitir_protocolo.html",{'destinatarios':destinatarios ,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro},context_instance=RequestContext(request))
            
            
        else:
            
        """
                    
    return render_to_response("emitir_protocolo.html",{'destinatarios':destinatarios ,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro},context_instance=RequestContext(request))
