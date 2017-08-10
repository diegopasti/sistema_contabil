# -*- encoding: utf-8 -*-
import locale

from datetime import date
from django.shortcuts import render_to_response,HttpResponse
from django.template import RequestContext
from django.http.response import Http404
from django.forms.models import model_to_dict

from servico.formularios import formulario_adicionar_servico, formulario_adicionar_plano
from servico.models import Servico, Plano
from django.core import serializers

import json

def cadastro_planos(request):
    formulario_plano = formulario_adicionar_plano()
    return render_to_response("servico/controle_planos.html",
                              {'formulario_plano': formulario_plano},
                              context_instance=RequestContext(request))

def consultar_planos(request):
    #if True: #request.is_ajax()
    planos = Plano.objects.all().filter(ativo=True)
    dados = []

    for item in planos:
        dict_obj = serializar_plano(item)
        dados.append(dict_obj)

    data = json.dumps(dados)
    return HttpResponse(data, content_type='application/json')
    #else:
    #raise Http404

def adicionar_plano(request):
    if request.is_ajax():
        plano = Plano()
        plano.nome = request.POST["plano"].upper()
        plano.descricao = request.POST["descricao"].upper()
        response_dict = executar_operacao(plano, "save")
        if response_dict['message'] != True:
            response_dict['message'] = serializar_plano(response_dict['message'])
        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

def atualizar_plano(request):
    if request.is_ajax():
        plano = Plano.objects.get(pk=int(request.POST["plano[id]"]))
        plano.nome = request.POST["plano[nome]"]
        plano.descricao = request.POST["plano[descricao]"]
        plano.servicos = request.POST["servicos"]

        response_dict = executar_operacao(plano, "save")
        if response_dict['message'] != True:
            response_dict['message'] = serializar_plano(response_dict['message'])
        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

def excluir_plano(request):
    if request.is_ajax():
        plano_id = request.POST["plano_id"]
        plano = Plano.objects.get(pk=int(plano_id))
        nome = plano.nome
        response_dict = executar_operacao(plano,"delete")
        response_dict['message'] = plano_id
        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

def serializar_plano(plano):
    texto = {}
    texto['id'] = str(plano.id)
    texto['nome'] = plano.nome
    texto['descricao'] = plano.descricao
    texto['data_cadastro'] = str(plano.data_cadastro.strftime("%Y-%m-%d"))
    texto['hora_cadastro'] = str(plano.data_cadastro.strftime("%H:%M:%S"))

    try:
        texto['servicos'] = [int(x) for x in plano.servicos.split(";")]
    except:
        texto['servicos'] = []

    if plano.cadastrado_por_id != 0:
        texto['cadastrado_por'] = plano.cadastrado_por
    else:
        texto['cadastrado_por'] = "ADMINISTRADOR"

    texto['data_ultima_alteracao'] = str(plano.ultima_alteracao.strftime("%Y-%m-%d"))
    texto['hora_ultima_alteracao'] = str(plano.ultima_alteracao.strftime("%H:%M:%S"))

    if plano.cadastrado_por_id != 0:
        texto['alterado_por'] = plano.alterado_por
    else:
        texto['alterado_por'] = 'ADMINISTRADOR'

    return texto


def cadastro_servico(request):
    erro = False
    servicos = []#Servico.objects.all()
    formulario_servico = formulario_adicionar_servico()

    return render_to_response("preferencias/cadastro_servicos.html",
                              {'dados': servicos,'formulario':formulario_servico,'erro':erro},
                              context_instance=RequestContext(request))


def adicionar_servico(request):
    if request.is_ajax():
        servico = Servico()
        servico.nome = request.POST["servico"]
        servico.descricao = request.POST["descricao"]
        response_dict = executar_operacao(servico, "save")
        response_dict['message'] = response_dict['message'].id
        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

def alterar_servico(request,servico_id):
    if request.is_ajax():
        servico = Servico.objects.get(pk=int(servico_id))
        servico.nome = request.POST["servico"]
        servico.descricao = request.POST["descricao"]
        response_dict = executar_operacao(servico, "save")
        response_dict['message'] = response_dict['message'].id
        return HttpResponse(json.dumps(response_dict))

        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

def excluir_servico(request,servico_id):
    if request.is_ajax():
        servico = Servico.objects.get(pk=int(servico_id))
        nome = servico.nome
        response_dict = executar_operacao(servico,"delete")
        response_dict['message'] = response_dict['message'].id
        return HttpResponse(json.dumps(response_dict))

    else:
        raise Http404

def executar_operacao(registro,operacao):
    response_dict = {}
    if operacao == "save":
        metodo_selecionado = registro.save
        menssage_sucesso = "Registro adicionado com Sucesso!"
        menssage_falha = "Erro! Registro não pode ser Salvo.\n"

    elif operacao == "delete":
        metodo_selecionado = registro.delete
        menssage_sucesso = "Registro apagado com Sucesso!"
        menssage_falha = "Erro! Registro não pode ser Salvo.\n"

    try:
        metodo_selecionado();
        response_dict['success'] = True
        response_dict['message'] = registro

    except Exception as e:
        response_dict['success'] = False
        response_dict['message'] = menssage_falha+str(e)
    return response_dict

def consultar_servicos(request):
    if True:#request.is_ajax():
        servicos = Servico.objects.all()
        dados = []
        for item in servicos:
            dict_obj = model_to_dict(item)
            dados.append(dict_obj)
        data = json.dumps(dados)
        print("OLHA O QUE TA INDO: ",data)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404