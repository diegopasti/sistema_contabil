# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''

from datetime import date
import datetime
from decimal import Decimal
import json
import os
import time

from django.contrib import messages
from django.core import serializers
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from entidade.formularios import formulario_emitir_protocolo, formulario_confirmar_entrega
from entidade.models import entidade, contato, localizacao_simples  # , localizacao
from entidade.views import verificar_erros_formulario
from protocolo.formularios import formulario_gerar_relatorio
from protocolo.models import protocolo, item_protocolo, item_protocolo_serializer
from sistema_contabil.settings import BASE_DIR


#from sistema_contabil.settings import BASE_DIR, STATIC_URL
#from endereco.models import localizacao
def get_detalhes_protocolo(request,protocolo_id):
    #if request.is_ajax():
    resultado = {}
    documentos = item_protocolo.objects.filter(protocolo_id=protocolo_id)
    p = protocolo.objects.get(pk=protocolo_id)
    
    if documentos.count() != 0:
        lista =[]
        for item in documentos:
            lista.append([item.documento,item.complemento,item.referencia,item.vencimento,item.valor])
            
        resultado['data'] = lista
        resultado['emitido_por'] = p.emitido_por
        data = json.dumps(resultado)
        
    else:
        print "Nenhum detalhe encontrado"
                
    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')

    #else:
    #    print "tentaram acessar os detalhes sem ser do jeito certo.."
    #    raise Http404
    

def validar_temporalidade(data_primeira_operacao,hora_primeira_operacao,data_segunda_operacao,hora_segunda_operacao):
    dp = data_primeira_operacao
    tp = hora_primeira_operacao
    
    ds = data_segunda_operacao
    ts = hora_segunda_operacao
        
    primeiro_datetime = datetime.datetime(dp.year,dp.month,dp.day,tp.hour,tp.minute,tp.second)
    segundo_datetime = datetime.datetime(ds.year,ds.month,ds.day,ts.hour,ts.minute,ts.second)
    
    return primeiro_datetime < segundo_datetime

def cadastro_protocolo(request):

    erro = False
    if (request.method == "POST"):
        
        form_entrega = formulario_confirmar_entrega()
        form_relatorio = formulario_gerar_relatorio()
        
        if 'gerar_relatorio' in request.POST:
            form_relatorio = formulario_gerar_relatorio(request.POST)
            
            if form_relatorio.is_valid(): 
                filtro_por_cliente = form_relatorio['filtrar_por_cliente'].value().upper()
                filtro_por_status = form_relatorio['filtrar_por_status'].value().upper()
                filtro_por_data_desde = form_relatorio['filtrar_desde'].value()
                filtro_por_operacao = form_relatorio['filtrar_por_operacao'].value()
                filtro_por_data_ate = form_relatorio['filtrar_ate'].value()
                 
                if filtro_por_cliente == '':
                    resultado = protocolo.objects.all()
                
                else:
                    resultado = protocolo.objects.filter(destinatario_id=filtro_por_cliente)
                    
                if filtro_por_status == 'CONFIRMADOS':
                    resultado = resultado.filter(situacao=1)
                
                elif filtro_por_status == 'ABERTOS':
                    resultado = resultado.filter(situacao=0)
                
                if filtro_por_data_desde != "":
                    filtro_por_data_desde = converte_formato_data(filtro_por_data_desde)
                    print 'emitidos desde: ',filtro_por_data_desde
                    
                    if filtro_por_operacao == "EMITIDOS":
                        resultado = resultado.filter(data_emissao__gte=filtro_por_data_desde)   
                    else:
                        resultado = resultado.filter(data_recebimento__gte=filtro_por_data_desde)
                    
                
                if filtro_por_data_ate != "":
                    filtro_por_data_ate = converte_formato_data(filtro_por_data_ate)
                    
                    if filtro_por_operacao == "EMITIDOS":
                        resultado = resultado.filter(data_emissao__lte=filtro_por_data_ate)
                    else:
                        resultado = resultado.filter(data_recebimento__lte=filtro_por_data_ate)
                    print 'emitidos ate: ',filtro_por_data_ate
                    
                
                #print 'resultados: '                
                #for item in resultado:
                #    print "Veja: ",item
                
                form_entrega = formulario_confirmar_entrega()
                form_relatorio = formulario_gerar_relatorio()
                
                return gerar_relatorio_simples(request,resultado)
                
                
            
        elif 'confirmar_protocolo' in request.POST:
            form_entrega = formulario_confirmar_entrega(request.POST)
            p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))
            
            if form_entrega.is_valid(): 
                p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))
                p.situacao = True
                p.recebido_por = form_entrega['recebido_por'].value().upper()
                
                data = form_entrega['data_entrega'].value()
                data = data.replace(" ","")
                tempo = form_entrega['hora_entrega'].value()
                
                if data != "":
                    dia = int(data[:2])
                    mes = int(data[3:5])
                    ano = int(data[6:])
                    data_entrega = datetime.date(ano,mes,dia)
                
                    if tempo != "":
                        tempo = tempo.split(':')
                        hora = int(tempo[0])
                        minuto = int(tempo[1])
                        hora_entrega = datetime.time(hora,minuto)
                        
                        if validar_temporalidade(p.data_emissao,p.hora_emissao,data_entrega,hora_entrega):
                            p.data_recebimento = data_entrega
                            p.hora_recebimento = hora_entrega
                            p.save()
                        
                        else:
                            messages.add_message(request, messages.SUCCESS, "Erro! Horário da entrega não pode ser anterior a emissão.")
                            erro = True
                    
                    else:
                        print "foi informado somente o dia, que nao pode ser anterior ao da emissao"
                
            else:
                msg = verificar_erros_formulario(form_entrega)
                print "olha o erro: ",msg
                messages.add_message(request, messages.SUCCESS, msg)
                erro = True
            
        
        else:
            print "e uma requisicao mas sem name do form"
    else:
        form_entrega = formulario_confirmar_entrega()
        form_relatorio = formulario_gerar_relatorio()
        
    dados = list(protocolo.objects.all())#*50
    clientes = entidade.objects.all()[1:]
    return render_to_response("protocolo/cadastro_protocolo.html",{"form_entrega":form_entrega,"form_relatorio":form_relatorio,'clientes':clientes,'dados':dados,'erro':erro},context_instance=RequestContext(request))

"""
def imprimir_protocolo(request,emissor,destinatario,documentos,):
    from django.template import Context
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens")
"""

def gerar_relatorio_simples(request,resultado):
    from django_xhtml2pdf.utils import generate_pdf
    from django.template import Context
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens\\")
    
    print request.POST
    
    resultado = list(resultado)
    
    descricao_destinatario = ""
    descricao_periodo = ""
    
    
    
    if request.POST['filtrar_por_cliente'] != '':
        cliente = entidade.objects.get(pk=request.POST['filtrar_por_cliente']).nome_razao
        
        
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario +u"Relatório de Protocolos em aberto do cliente "+cliente
        else:
            descricao_destinatario = descricao_destinatario +u"Relatório de Protocolos do cliente "+cliente
    else:
        cliente = "TODOS"
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario +u"Relatório de protocolos em aberto dos clientes"
        else:
            descricao_destinatario = descricao_destinatario +u"Relatório de protocolos dos clientes"
        
    if request.POST['filtrar_desde'] != '':
        
        if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
            #descricao_periodo = descricao_periodo +"Emitidos desde "+request.POST['filtrar_desde']
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']
            
        elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']
    
    else:
        pass
        #if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
        #    descricao_periodo = descricao_periodo +" Emitidos"
            
        #elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
        #    descricao_periodo = descricao_periodo +"Recebidos"
            
    if request.POST['filtrar_ate'] != '':
        descricao_periodo = descricao_periodo +u" até "+request.POST['filtrar_ate']
    
    data = date.today() 
    hora = datetime.datetime.now().strftime("%H:%M")
    

    
    parametros = {'protocolos':resultado,
                  'path_imagens':path,
                  'emitido_por':'MARCELO',
                  'descricao_destinatario':descricao_destinatario,
                  
                  
                  'filtro_operacao':request.POST['filtrar_por_operacao'].capitalize(),
                  'filtro_status':request.POST['filtrar_por_status'].upper(),
                  'filtro_periodo':descricao_periodo,
                  'filtro_cliente':cliente,
                  
                  'data_emissao':data,
                  'hora_emissao':hora
                  
                  }
    context = Context(parametros)
    
    
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_relatorio_simples.html', file_object=resp,context=context)
    return result


def gerar_pdf(request, formulario,emissor, destinatario, protocolo):
    from django.template import Context# loader,Context, Template
    path = os.path.join(BASE_DIR, "arquivos_estaticos\imagens\\")
    
    print protocolo.data_emissao, protocolo.hora_emissao

    
    parametros = {
                  'emissor_nome':emissor.nome,
                  'emissor_cpf_cnpj':formatar_cpf_cnpj(emissor.cpf_cnpj),
                  'emissor_endereco':emissor.endereco,
                  'emissor_contatos':emissor.contatos,
                  
                  'destinatario_nome':destinatario.nome,
                  'destinatario_cpf_cnpj':destinatario.cpf_cnpj,
                  'destinatario_endereco':destinatario.endereco,
                  'destinatario_complemento':destinatario.complemento,
                  'destinatario_contatos':destinatario.contatos,
                  
                  'codigo_protocolo':destinatario.codigo_protocolo,
                  'emitido_por':'Marcelo',
                  'data_emissao':protocolo.data_emissao,
                  'hora_emissao':protocolo.hora_emissao,
                  
                  
                  'recebido_por':"",#recebido_por,
                  'identificacao':"",#identidade,
                  'data_entrega':"",#data_entrega,
                  'hora_entrega':"",#hora_entrega,
                  
                  'documentos':formulario.temporarios,
                  #'documentos':[
                  #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                  #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                  #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                  #              ],
                  #'formulario_protocolo':"Nada por enquanto",
                  #'erro':"sem erros tambem",
                  #'path':path,
                  
                  'path_imagens':path
                   
                }
    
    c = Context(parametros)
    
    # RENDERIZAR NORMAL
    #return render_to_response('protocolo/imprimir_protocolo.html', c)
    
    # RENDERIZAR PDF
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp,context=c)
    return result
    


class ParametroProtocolo:
    
    nome             = None
    contatos         = None
    endereco         = None
    cpf_cnpj         = None
    complemento      = None
    codigo_protocolo = None
    
    
    
    

def criar_protocolo(request,formulario):
    emissor = entidade.objects.get(pk=1)
    parametro_emissor = ParametroProtocolo()
    
    parametro_emissor.nome = emissor.nome_razao
    parametro_emissor.cpf_cnpj = emissor.cpf_cnpj
    
    endereco = localizacao_simples.objects.get(pk=emissor.endereco_id)
    
    endereco = "%s, %s, %s, %s, %s - %s"%(endereco.logradouro,endereco.numero,endereco.bairro,endereco.municipio, endereco.estado, formatar_cep(endereco.cep))
    parametro_emissor.endereco = endereco
    parametro_emissor.contatos = ["(27) 98834-2005","(27) 3022-1224"]

    p = protocolo()
    p.emissor = emissor
    p.emitido_por = "MARCELO"
    
    destinatario = formulario['entidade_destinatario'].value()
    
    if '|' in destinatario:
        campos = destinatario.split("|")
        
        cliente_id = -1
        
        destinatario             = ParametroProtocolo()
        destinatario.nome        = campos[0].upper()
        destinatario.cpf_cnpj    = formatar_cpf_cnpj(campos[1])
        destinatario.endereco    = campos[2].title()
        destinatario.complemento = ""
        
        destinatario.codigo_protocolo = "AVULSO"
        
        if campos[3] == "":
            destinatario.contatos = []
        else:
            destinatario.contatos = [campos[3]]
        
        #print "olha o que veio: ",formulario['entidade_destinatario'].value() 
        p.destinatario = None
        p.nome_avulso = destinatario.nome
        p.endereco_avulso = destinatario.endereco
        p.contatos_avulso = campos[3]
        
        p.numeracao_destinatario = destinatario.codigo_protocolo
    
    else:
        id_destinatario = int(destinatario[:destinatario.find(" - ")])
        registro = entidade.objects.get(pk=id_destinatario)
        cliente_id = id_destinatario
        
        destinatario             = ParametroProtocolo()
        destinatario.nome        = registro.nome_razao.upper()
        destinatario.cpf_cnpj    = formatar_cpf_cnpj(registro.cpf_cnpj)
        
        registro_endereco = localizacao_simples.objects.get(pk=registro.endereco_id)
        endereco = "%s, %s, %s, %s, %s - %s"%(registro_endereco.logradouro,registro_endereco.numero,registro_endereco.bairro,registro_endereco.municipio, registro_endereco.estado, formatar_cep(registro_endereco.cep))
        
        destinatario.endereco    = endereco.title()
        destinatario.complemento = registro_endereco.complemento.title()
        
        destinatario.codigo_protocolo = "%05d"%(registro.numeracao_protocolo)

        destinatario.contatos = []
        
        for item in contato.objects.filter(entidade=registro):
            destinatario.contatos.append(item.numero)
        
        p.destinatario = registro  
        p.numeracao_destinatario = destinatario.codigo_protocolo
        
    p.save()
    
    if cliente_id != -1:
        registro = entidade.objects.get(pk=cliente_id)
        registro.numeracao_protocolo = registro.numeracao_protocolo + 1
        registro.save()
    
    
    for item in formulario.temporarios:
        item.protocolo_id = p.id
        
        print item.documento,item.referencia,item.vencimento,item.valor,item.complemento
        item.save()
    
    return parametro_emissor,destinatario,p
         

def emitir_protocolo(request,numero_item):
    numero_item = int(numero_item)
    erro = False
    destinatarios = entidade.objects.all()[1:]  
    
    if (request.method == "POST"):
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST)
        
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
            
            else:
                msg = verificar_erros_formulario(formulario_protocolo)
                messages.add_message(request, messages.SUCCESS, msg)
                erro = True
            
            
        elif 'gerar_protocolo' in request.POST:
            emissor, destinatario, protocolo = criar_protocolo(request, formulario_protocolo)
            resposta_pdf = gerar_pdf(request,formulario_protocolo, emissor, destinatario, protocolo)
            return resposta_pdf
        
        elif 'excluir_item' in request.POST:
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            #print formulario_protocolo["excluir_item"]
            
            try:
                formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[int(formulario_protocolo["excluir_item"].value())])
            except:
                pass
            
    else:
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_protocolo.limpar_temporarios()
                    
    return render_to_response("protocolo/emitir_protocolo.html",{'destinatarios':destinatarios ,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro},context_instance=RequestContext(request))


def salvar_itens_protocolos(protocolo,itens_protocolo):
    for item in itens_protocolo:                
        item.protocolo = protocolo
        item.save()
        
        
        
        
        
        
"""
 
 COISAS QUE PODEM SER COLOCADAS EM OUTROS LUGARES

"""

def converte_formato_data(data):
    nova_data = data[6:]+"-"+data[3:5]+'-'+data[:2]
    return nova_data

def formatar_cep(cep):
    cep_formatado = ""+cep[:2]+"."+cep[2:5]+"-"+cep[5:]
    return cep_formatado

def formatar_cpf_cnpj(codigo):
    if len(codigo) == 11:
        codigo_formatado = codigo[:3]+"."+codigo[3:6]+"."+codigo[6:9]+"-"+codigo[9:]
    else:
        codigo_formatado = codigo[:2]+"."+codigo[2:5]+"."+codigo[5:8]+"/"+codigo[9:13]+"-"+codigo[13:]
    return codigo_formatado

