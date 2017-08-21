# -*- encoding: utf-8 -*-
'''
Created on 17 de ago de 2017

@author: Diego
'''
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context
from django_xhtml2pdf.utils import generate_pdf

from entidade.models import entidade
from protocolo.models import protocolo
from sistema_contabil.settings import BASE_DIR


def report_protocols_per_documents(request, form):
    images_path = os.path.join(BASE_DIR, "arquivos_estaticos/imagens")

    filtro_cliente = form['filtrar_por_cliente'].value().upper()
    filtro_status  = form['filtrar_por_status'].value().upper()
    filtro_desde = form['filtrar_desde'].value()
    filtro_operacao = form['filtrar_por_operacao'].value()
    filtro_ate = form['filtrar_ate'].value()
    filtro_documento = form['filtrar_documentos'].value()

    if filtro_cliente == 'TODOS':
        filtro_cliente = "TODOS CLIENTES"
    else:
        print("VEJA O CLIENTE: ", filtro_cliente)
        cliente = entidade.objects.get(pk=int(filtro_cliente))
        filtro_cliente = cliente.nome_razao



    #from django_xhtml2pdf.utils import generate_pdf
    #from django.template import Context
    #path = os.path.join(BASE_DIR, "arquivos_estaticos/imagens/")


    protocols_list = list(protocolo.objects.all())
    print("É ISSO ESTOU GERANDO O RELATORIO", protocols_list)


    """
    resultado = list(resultado)

    descricao_destinatario = ""
    descricao_periodo = ""

    if request.POST['filtrar_por_cliente'] != '':
        cliente = entidade.objects.get(pk=request.POST['filtrar_por_cliente']).nome_razao

        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario + u"Relatório de Protocolos em aberto do cliente " + cliente
        else:
            descricao_destinatario = descricao_destinatario + u"Relatório de Protocolos do cliente " + cliente
    else:
        cliente = "TODOS"
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario + u"Relatório de protocolos em aberto dos clientes"
        else:
            descricao_destinatario = descricao_destinatario + u"Relatório de protocolos dos clientes"

    if request.POST['filtrar_desde'] != '':

        if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
            # descricao_periodo = descricao_periodo +"Emitidos desde "+request.POST['filtrar_desde']
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']

        elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']

    else:
        pass
        # if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
        #    descricao_periodo = descricao_periodo +" Emitidos"

        # elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
        #    descricao_periodo = descricao_periodo +"Recebidos"

    if request.POST['filtrar_ate'] != '':
        descricao_periodo = descricao_periodo + u" até " + request.POST['filtrar_ate']

    data = date.today()
    hora = datetime.datetime.now().strftime("%H:%M")
    
    
    parametros = {
        'protocolos': resultado,
        'path_imagens': path,
        'emitido_por': 'MARCELO',
        'descricao_destinatario': descricao_destinatario,
        
        'filtro_operacao': request.POST['filtrar_por_operacao'].capitalize(),
        'filtro_status': request.POST['filtrar_por_status'].upper(),
        'filtro_periodo': descricao_periodo,
        'filtro_cliente': cliente,
        
        'data_emissao': data,
        'hora_emissao': hora
    }
    """

    parametros = {
        'protocols_list':protocols_list,
        'images_path':images_path,
        'filtro_cliente':filtro_cliente,
        'filtro_status':filtro_status,
        'filtro_desde':filtro_desde,
        'filtro_operacao':filtro_operacao,
        'filtro_ate':filtro_ate,
        'filtro_documento':filtro_documento,
    }
    context = Context(parametros)
    return render_to_response('protocolo/report/report_per_documents.html', context)


    #resp = HttpResponse(content_type='application/pdf')
    #result = generate_pdf('protocolo/imprimir_relatorio_simples.html', file_object=resp, context=context)
    #return result