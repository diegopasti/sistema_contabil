# -*- encoding: utf-8 -*-

import json

from django.contrib import messages
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from entidade.formularios import formulario_cadastro_entidade_completo
from entidade.models import entidade, contato, localizacao, endereco, estado, municipio, bairro
from utilitarios.internet import consultar_codigo_postal


def index(request):
    return render_to_response("index.html")

def cadastro_entidades(request):
    return render_to_response("cadastro_entidades.html")

def consultar_cep(request,codigo_postal):    
   
    if request.is_ajax():
        codigo_postal = codigo_postal.replace(".","")
        codigo_postal = codigo_postal.replace("-","")
        
        resultado = endereco.objects.filter(cep=codigo_postal)
        
        #print "resultado no banco: ",resultado.count()
        
        if resultado.count() == 0:
            resultado = consultar_codigo_postal(codigo_postal)
            registro_estado = estado.objects.get(sigla=resultado[3])            
            registro_pais = registro_estado.pais.nome
            registro_municipio = municipio.objects.select_related().get(estado=registro_estado,nome=resultado[2])
            codigo_municipal = registro_municipio.codigo_ibge
            resultado.append(codigo_municipal)
            resultado.append(registro_pais)
            
            
            registro_bairro = bairro.objects.select_related().get(municipio=registro_municipio,nome=resultado[1])
                        
            registro_endereco = endereco(
                                 cep = codigo_postal,
                                 bairro = registro_bairro,
                                 nome = resultado[0]
                                 )
            registro_endereco.save()
            
        
        else:
            registro_endereco = resultado[0]
            registro_bairro = bairro.objects.get(id=registro_endereco.bairro_id)
            registro_cidade = registro_bairro.municipio  #municipio.objects.get(id=registro_bairro.municipio_id)
            registro_estado = registro_cidade.estado     # estado.objects.get(id=registro_cidade.estado_id)
            resultado = [registro_endereco.nome,registro_bairro.nome,registro_cidade.nome,registro_estado.sigla,registro_cidade.codigo_ibge,registro_estado.pais.nome]
            #print "Deu certo: ",resultado
        
        data = json.dumps(resultado)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def remover_simbolos(texto):
    texto = texto.replace(".","")
    texto = texto.replace(",","")
    texto = texto.replace("-","")
    return texto

def adicionar_entidade(request):
    if (request.method == "POST"):
                
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)        
        codigo_postal = remover_simbolos(formulario['cep'].value())
                
        if formulario.is_valid():
            
            registro_entidade = entidade()
            registro_entidade.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
            registro_entidade.nome_razao = formulario.cleaned_data['nome_razao']
            registro_entidade.apelido_fantasia = formulario.cleaned_data['apelido_fantasia']
            registro_entidade.tipo_registro = formulario.cleaned_data['tipo_registro']
            registro_entidade.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
            
            validacao = False
            try:
                registro_entidade.save()
                validacao = True
                
            except IntegrityError as excecao:
                if "cpf_cnpj" in excecao.message:
                    msg = "Erro! cpf ou cnpj já existe no cadastro!"
                
                else:
                    msg = excecao.message
                    
            if validacao:
                registro_contato = contato(
                    entidade = registro_entidade,#entidade.objects.get(pk=registro_entidade.id),
                    nome_contato = registro_entidade.nome_razao,
                    tipo_contato = formulario.cleaned_data['tipo_contato'],
                    numero       = remover_simbolos(formulario.cleaned_data['numero_contato']),
                    cargo_setor  = formulario.cleaned_data['cargo_setor'],
                    email        = formulario.cleaned_data['email'],
                )                        
                #registro_contato.save()        
                            
                codigo_postal = remover_simbolos(formulario.cleaned_data['cep'])
                
                print "Tamo procurando o cep: ",codigo_postal
                cep_id = endereco.objects.filter(cep=codigo_postal)
                print "Cep ID: ",cep_id
                
                registro_localizacao = localizacao(
                    cep_id      = cep_id,
                    numero      = formulario.cleaned_data['numero_endereco'],
                    complemento = formulario.cleaned_data['complemento'],
                    
                    )
                
            
                #endereco = formulario.cleaned_data['endereco']
                
                bairro = formulario.cleaned_data['bairro']
                
                municipio = formulario.cleaned_data['municipio']
                codigo_municipio = remover_simbolos(formulario.cleaned_data['codigo_municipio'])
                estado = formulario.cleaned_data['estado']
                
                pais = formulario.cleaned_data['pais']
                tipo_contato = formulario.cleaned_data['tipo_contato']
                numero_contato = remover_simbolos(formulario.cleaned_data['numero_contato'])
                cargo_setor = formulario.cleaned_data['cargo_setor']
                email = formulario.cleaned_data['email']
            
                messages.add_message(request, messages.SUCCESS, "Registro salvo com sucesso!")
                
            else:
                messages.add_message(request, messages.SUCCESS, msg)
        
        else:
            
            msg = ""            
            for campo in formulario:
                erros = campo.errors.as_data()
                
                
                if erros != []:
                    
                    erro = erros[0][0]
                    
                    if 'email' in erro:
                        msg = "Erro! "+unicode(erro)
                    else:
                        msg = campo.label+" "+erro
                    messages.add_message(request, messages.SUCCESS, msg)
                    break
    
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contato  = form_adicionar_contato()
        
    return render_to_response("adicionar_entidade.html",{'formulario':formulario},context_instance=RequestContext(request))
        
    #return render_to_response("adicionar_entidade.html",{'formulario_entidade':formulario_entidade,'formulario_contato':formulario_contato},context_instance=RequestContext(request))   
        
