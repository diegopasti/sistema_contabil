# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from honorario.forms import FormContrato
from sistema_contabil import settings
from servico.models import Contrato
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
        response_dict['data-object'] = serializers.serialize('json', [object], fields=tuple(list_fields))
        response_dict['data-object'] = response_dict['data-object'][1:-1]

    else:
        response_dict['data-object'] = None
    return response_dict


def get_lista_contratos(request):
    lista_contratos = Contrato.objects.all()
    filter_request(request)
    response_dict = {}#response_format_success_message(None, )
    print("VEJA OS CONTRATOS: ",lista_contratos)
    # response_dict = response_format_error("Formulário com dados inválidos.")
    return HttpResponse(json.dumps(response_dict))

def salvar_contrato(request):
    print("VEJA O REQUEST: ",request.POST)
    filter_request(request)
    response_dict = {}  # response_format_success_message(None, )
    # response_dict = response_format_error("Formulário com dados inválidos.")
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