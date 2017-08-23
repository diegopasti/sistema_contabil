# -*- encoding: utf-8 -*-
import datetime

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

'''Temporario'''
def get_lista_indicacoes(request,cliente_id):

    print ("CHEGANDO NAS INDICACOES")
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

        """
        else:
            response_indicacao = {}
            response_indicacao['cliente_id'] = None
            response_indicacao['indicacao']['nome_empresa'] = None
            response_indicacao['indicacao']['data_registro'] = None
            response_indicacao['indicacao']['taxa_desconto'] = None
            response_indicacao['indicacao']['indicacao_ativa'] = None
            response_indicacao['indicacao']['cadastrado_por'] = None
            response_indicacao['indicacao']['ultima_alteracao'] = None
            response_indicacao['indicacao']['alterador_por'] = None
        """
        response_dict.append(response_indicacao)
    return HttpResponse(json.dumps(response_dict))


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
                filtro_por_documento = form_relatorio['filtrar_documentos'].value()

                if len(filtro_por_documento) != 0:
                    return report_protocols_per_documents(request, form_relatorio)

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
                    print 'emitidos desde: ', filtro_por_data_desde

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
                    print 'emitidos ate: ', filtro_por_data_ate

                # print 'resultados: '
                # for item in resultado:
                #    print "Veja: ",item

                form_entrega = formulario_confirmar_entrega()
                form_relatorio = formulario_gerar_relatorio()

                return gerar_relatorio_simples(request, resultado)
            else:
                print("DEU ERRO? ", form_relatorio.errors)

        elif 'confirmar_protocolo' in request.POST:
            form_entrega = formulario_confirmar_entrega(request.POST)
            p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))

            if not p.situacao:
                # messages.add_message(request, messages.SUCCESS, "Protocolo já foi confirmado!")
                if form_entrega.is_valid():
                    p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))
                    p.situacao = True
                    p.recebido_por = form_entrega['recebido_por'].value().upper()
                    p.doc_receptor = form_entrega['doc_receptor'].value()

                    data = form_entrega['data_entrega'].value()
                    data = data.replace(" ", "")
                    tempo = form_entrega['hora_entrega'].value()

                    if data != "":
                        dia = int(data[:2])
                        mes = int(data[3:5])
                        ano = int(data[6:])
                        data_entrega = datetime.date(ano, mes, dia)

                        if tempo != "":
                            tempo = tempo.split(':')
                            hora = int(tempo[0])
                            minuto = int(tempo[1])
                            hora_entrega = datetime.time(hora, minuto)

                            if validar_temporalidade(p.data_emissao, p.hora_emissao, data_entrega, hora_entrega):
                                p.data_recebimento = data_entrega
                                p.hora_recebimento = hora_entrega
                                p.save()
                                return HttpResponseRedirect('/protocolo')

                            else:
                                messages.add_message(request, messages.SUCCESS,
                                                     "Erro! Horário da entrega não pode ser anterior a emissão.")
                                erro = True

                        else:
                            print "foi informado somente o dia, que nao pode ser anterior ao da emissao"

                else:
                    msg = verificar_erros_formulario(form_entrega)
                    messages.add_message(request, messages.SUCCESS, msg)
                    erro = True
            else:
                return HttpResponseRedirect('/protocolo')

        else:
            # print "e uma requisicao mas sem name do form"
            return HttpResponseRedirect('protocolo/cadastro_protocolo.html')

    else:
        form_entrega = formulario_confirmar_entrega()
        form_relatorio = formulario_gerar_relatorio()
        # print("VEJA O NOVO CAMPO: ",form_relatorio.filtrar_documentos)

    dados = list(protocolo.objects.all())  # *30
    clientes = entidade.objects.all()[1:]
    return render_to_response("protocolo/cadastro_protocolo.html",
                              {"form_entrega": form_entrega, "form_relatorio": form_relatorio, 'clientes': clientes,
                               'dados': dados, 'erro': erro}, context_instance=RequestContext(request))

'''FIM Temporario'''

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