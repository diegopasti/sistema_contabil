# -*- encoding: utf-8 -*-

from django.core.checks import messages
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext

from entidade.models import entidade
from entidade.views import verificar_erros_formulario
from honorario.forms import FormContrato
from honorario.models import Contrato, Indicacao
from nucleo.initial_data import protocolo
from protocolo.formularios import formulario_confirmar_entrega, formulario_gerar_relatorio
from protocolo.report import report_protocols_per_documents
from protocolo.views import converte_formato_data, gerar_relatorio_simples, validar_temporalidade
from sistema_contabil import settings
from django.core import serializers
import json


def filter_request(request, formulary=None):
    if request.is_ajax() or settings.DEBUG:
        if formulary is not None:
            form = formulary(request.POST)
            if form.is_valid():
                return True, form
            else:
                return False, form
        else:
            return True, True
    else:
        raise Http404


def response_format_success_message(object,list_fields):
    return response_format(True, '', object, list_fields)


def response_format_error_message(message):
    return response_format(False, message, None, None)


def response_format(result,message,object,list_fields):
    response_dict = {}
    response_dict['success'] = result
    response_dict['message'] = message
    if result:
        if list_fields is not None:
            response_dict['data-object'] = serializers.serialize('json', [object], fields=tuple(list_fields))
        else:
            response_dict['data-object'] = serializers.serialize('json', [object])
        response_dict['data-object'] = response_dict['data-object'][1:-1]

    else:
        response_dict['data-object'] = None
    return response_dict


def get_lista_contratos(request):
    lista_clientes = entidade.objects.all()
    response_dict = []
    for item in lista_clientes:

        response_cliente = {}
        response_cliente['cliente_id'] = item.id
        response_cliente['cliente_nome'] = item.nome_razao
        response_cliente['selecionado'] = False
        contrato = Contrato.objects.filter(cliente=item.id)

        if len(contrato) != 0:
            contrato = contrato[0]
            response_cliente['contrato'] = {}
            response_cliente['plano'] = contrato.plano.nome
            response_cliente['indicacoes'] = []
            response_cliente['contrato']['tipo_cliente'] = contrato.tipo_cliente

            if(contrato.vigencia_inicio): response_cliente['contrato']['vigencia_inicio'] = str(contrato.vigencia_inicio.strftime('%d/%m/%Y'))

            if (contrato.vigencia_fim): response_cliente['contrato']['vigencia_fim'] = str(contrato.vigencia_fim.strftime('%d/%m/%Y'))
            response_cliente['contrato']['taxa_honorario'] = contrato.taxa_honorario

            if (contrato.taxa_honorario): response_cliente['contrato']['taxa_honorario'] = float(contrato.taxa_honorario)
            if (contrato.valor_honorario): response_cliente['contrato']['valor_honorario'] = float(contrato.valor_honorario)

            response_cliente['contrato']['dia_vencimento'] = contrato.dia_vencimento
            response_cliente['contrato']['data_vencimento'] = contrato.data_vencimento
            response_cliente['contrato']['desconto_temporario'] = float(contrato.desconto_temporario)

            #if (contrato.desconto_indicacoes):
            response_cliente['contrato']['desconto_indicacoes'] = float(contrato.desconto_indicacoes)
            print("VEJA O QUE TEM DE INDICACAO: ", response_cliente['contrato']['desconto_indicacoes'])

            if (contrato.desconto_inicio): response_cliente['contrato']['desconto_inicio'] = str(contrato.desconto_inicio.strftime('%d/%m/%Y'))
            if (contrato.desconto_fim): response_cliente['contrato']['desconto_fim'] = str(contrato.desconto_fim.strftime('%d/%m/%Y'))

            response_cliente['contrato']['cadastrado_por'] = contrato.cadastrado_por.nome_razao
            response_cliente['contrato']['data_cadastro'] = str(contrato.data_cadastro.strftime('%d/%m/%Y'))
            response_cliente['contrato']['ultima_alteracao'] = str(contrato.ultima_alteracao.strftime('%d/%m/%Y'))
            response_cliente['contrato']['alterado_por'] = contrato.alterado_por.nome_razao

        else:
            response_cliente['contrato'] = {}
            response_cliente['plano'] = None
            response_cliente['indicacoes'] = []
            response_cliente['contrato']['tipo_cliente'] = None
            response_cliente['contrato']['vigencia_inicio'] = None
            response_cliente['contrato']['vigencia_fim'] = None
            response_cliente['contrato']['taxa_honorario'] = None
            response_cliente['contrato']['valor_honorario'] = None
            response_cliente['contrato']['dia_vencimento'] = None
            response_cliente['contrato']['data_vencimento'] = None
            response_cliente['contrato']['desconto_temporario'] = None
            response_cliente['contrato']['desconto_inicio'] = None
            response_cliente['contrato']['desconto_fim'] = None
            response_cliente['contrato']['desconto_indicacoes'] = None
            response_cliente['contrato']['cadastrado_por'] = None
            response_cliente['contrato']['data_cadastro'] = None
            response_cliente['contrato']['ultima_alteracao'] = None
            response_cliente['contrato']['alterado_por'] = None

        response_dict.append(response_cliente)
    return HttpResponse(json.dumps(response_dict))


def get_lista_indicacoes(request,cliente_id):

    id_cliente = int(cliente_id)
    lista_indicacoes = Indicacao.objects.filter(cliente=id_cliente)
    response_dict = []
    for indicacao in lista_indicacoes :
        response_indicacao = {}
        response_indicacao['cliente_id'] = indicacao.cliente.id
        response_indicacao['indicacao'] = {}
        response_indicacao['indicacao']['selecionado'] = ''
        response_indicacao['indicacao']['nome_razao'] = indicacao.indicacao.nome_razao
        response_indicacao['indicacao']['data_cadastro'] = str(indicacao.data_cadastro.strftime('%d/%m/%Y'))
        response_indicacao['indicacao']['taxa_desconto'] = float(indicacao.taxa_desconto)
        response_indicacao['indicacao']['indicacao_ativa'] = indicacao.indicacao_ativa
        response_indicacao['indicacao']['cadastrado_por'] = indicacao.cadastrado_por.nome_razao
        response_indicacao['indicacao']['ultima_alteracao'] = str(indicacao.ultima_alteracao.strftime('%d/%m/%Y'))
        response_indicacao['indicacao']['alterador_por'] = indicacao.alterado_por.nome_razao
        response_dict.append(response_indicacao)
    return HttpResponse(json.dumps(response_dict))

def salvar_indicacao (request):

    empresa = request.POST['empresa']
    taxa_desconto = request.POST['taxa_desconto']
    cliente_id = request.POST['cliente_id']

    indicacao = Indicacao()
    indicacao.cliente_id = int(cliente_id)
    indicacao.indicacao_id = int(empresa)
    indicacao.taxa_desconto = float(taxa_desconto)

    try:
        indicacao.save()
        response_dict = response_format_success_message(indicacao,['indicacao','cliente','taxa_desconto'])
    except:
        response_dict = response_format_error_message('Deu Erro')

    return HttpResponse(json.dumps(response_dict))


def salvar_contrato(request):
    result, form = filter_request(request,FormContrato)
    if result:
        contrato = form.form_to_object()
        cliente = entidade.objects.get(pk=int(request.POST['cliente']))
        contrato.cliente = cliente
        contrato.save()
        response_dict = response_format_success_message(contrato,None)
    else:
        print("VEJA OS ERROS: ",form.errors)
        response_dict = response_format_error_message("Formulário com dados inválidos.")

    return HttpResponse(json.dumps(response_dict))



"""
class ContratoAPI:

    def get_lista_contratos(request):
        lista_contratos = Contrato.objects.all()
        #response_dict = response_format_error("Formulário com dados inválidos.")
        return HttpResponse({'message':'Testando'})



    def register_user(request):
        resultado, form = AbstractAPI.filter_request(request, FormRegister)
        #print("VAMOS LA.. VEJA OS TESTS: ",request.POST)
        if resultado:
            #print("TA VALIDO")
            email = request.POST['email'].lower()
            senha = request.POST['password']
            if User.objects.check_available_email(email):
                #print("EMAIL TA DISPONIVEL")
                usuario = User.objects.create_contracting_user(email, senha)
                if usuario is not None:
                    activation_code = generate_activation_code(email)
                    send_generate_activation_code(email, activation_code)
                    response_dict = response_format_success(usuario, ['email'])
                else:
                    #print("USUARIO NAO TA CADASTRADO")
                    response_dict = response_format_error("Nao foi possivel criar objeto")
            else:
                #print("EMAIL TA INDISPONIVEL")
                response_dict = response_format_error("Email já cadastrado.")
        else:
            #print("FORMULARIO INCORRETO")
            response_dict = response_format_error("Formulário com dados inválidos.")
        return HttpResponse(json.dumps(response_dict))

    def register_delete(request, email):
        user = User.objects.get_user_email(email)
        if user is not None:
            user.delete()
            response_dict = response_format_error("Usuario deletado com sucesso.")
        else:
            response_dict = response_format_error("Usuario nao existe.")
        return HttpResponse(json.dumps(response_dict))
"""