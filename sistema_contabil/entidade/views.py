# -*- encoding: utf-8 -*-

import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from entidade.formularios import formulario_cadastro_entidade_completo, \
    formulario_emitir_protocolo, formulario_adicionar_item_protocolo
from entidade.models import entidade, contato, localizacao, endereco, estado, municipio, bairro, \
    item_protocolo, protocolo
from entidade.utilitarios import formatar_codificacao, remover_simbolos
from util.internet import consultar_codigo_postal


def index(request):
    return render_to_response("index.html")


"""
def adicionar_item_protocolo(request):
    
    print "cheguei no ajax carai!"
    if request.is_ajax():
        formulario_itens     = formulario_adicionar_item_protocolo(request.POST, request.FILES)
        
        if 'adicionar_item' in request.POST:
            if formulario_itens.is_valid():
                documento  = formulario_itens['documento'].value()
                referencia = formulario_itens['referencia'].value()
                vencimento = formulario_itens['vencimento'].value()
                valor      = formulario_itens['valor'].value()
                
                item            = item_protocolo()
                item.documento  = documento
                item.referencia = referencia
                item.vencimento = vencimento
                item.valor      = valor
            
                formulario_itens  = formulario_adicionar_item_protocolo()
                #itens_temporarios = [documento,referencia,vencimento,valor]
                                
                formulario_itens.temporarios.append(item)
                #formulario_itens.temporarios.append(itens_temporarios)
                
                messages.add_message(request, messages.SUCCESS, "Item adicionado com sucesso")
                
            else:
                msg = verificar_erros_formulario(formulario_itens)
                #print msg
                messages.add_message(request, messages.SUCCESS, msg)
        
    else:
        
    data = json.dumps(resultado)
        return HttpResponse(data, content_type='application/json')
    
    else:
        raise Http404
"""

def emitir_protocolo(request,numero_item):
    numero_item = int(numero_item)
    print "Tem argumento: ",numero_item
    
    #print "ve o que tem no request_post: ",request.POST," > ",type(request.POST)
    
    
    #itens_temporarios = []
    
    
    
    erro = False
    if (request.method == "POST"):
        
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST, request.FILES)
        formulario_itens     = formulario_adicionar_item_protocolo(request.POST, request.FILES)
        
        
        #print "ve o que tem no temporario: ",formulario_itens.temporarios
        
        if 'adicionar_item' in request.POST:
            if formulario_itens.is_valid():
                documento  = formulario_itens['documento'].value().upper()
                referencia = formulario_itens['referencia'].value()
                vencimento = formulario_itens['vencimento'].value()
                valor      = formulario_itens['valor'].value()
                complemento      = formulario_itens['complemento'].value().upper()
                
                item            = item_protocolo()
                item.documento  = documento
                item.complemento= complemento
                item.referencia = referencia
                item.vencimento = vencimento
                item.valor      = valor
                
                #if item.clean():
                #    item.save()
                #else:
                #    print "Deu problema pra salvar"
                
                formulario_itens  = formulario_adicionar_item_protocolo()
                #itens_temporarios = [documento,referencia,vencimento,valor]
                                
                formulario_itens.temporarios.append(item)
                
                #formulario_itens.temporarios.append(itens_temporarios)
                
                #messages.add_message(request, messages.SUCCESS, "Item adicionado com sucesso")
                
            else:
                msg = verificar_erros_formulario(formulario_itens)
                messages.add_message(request, messages.SUCCESS, msg)
                erro = True
        
        elif 'gerar_protocolo' in request.POST:
            
            if formulario_protocolo.is_valid():
                
                if formulario_itens.temporarios != []:
                    
                    novo_protocolo = protocolo()
                    novo_protocolo.emissor = entidade.objects.get(pk=26)
                    novo_protocolo.destinatario = entidade.objects.get(pk=formulario_protocolo['entidade_destinatario'].value())
                    
                    novo_protocolo.save()
                    
                    for item in formulario_itens.temporarios:
                        print item.documento,",",item.referencia,",",item.vencimento,",",item.valor
                        
                        item.protocolo = novo_protocolo
                        
                        
                        try:
                            item.save()
                        except Exception as erro:
                            print "Deu pau..",erro.message_dict
                                                    
                    
                    print "deu Certo sera?!"
                    messages.add_message(request, messages.SUCCESS, "Gerando protocolo")
                else:
                    messages.add_message(request, messages.SUCCESS, "Informe os documentos a ser enviado")
                
            else:
                msg = verificar_erros_formulario(formulario_protocolo)
                messages.add_message(request, messages.SUCCESS, msg)
        
    else:
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_itens     = formulario_adicionar_item_protocolo()
        
    if request.is_ajax():
        formulario_itens.temporarios.remove(formulario_itens.temporarios[numero_item])
        print "apaguei"
        
    dados = []
    
    return render_to_response("emitir_protocolo.html",{'dados':formulario_itens.temporarios,'formulario_protocolo':formulario_protocolo,'formulario_itens':formulario_itens,'erro':erro},context_instance=RequestContext(request))

def validar_objeto(registro):
    print "Campo: ",registro
    
    print registro.documento,",",registro.referencia,",",registro.vencimento,",",registro.valor,",",registro.protocolo.emissor.nome_razao
    
    try:
        registro.full_clean()
        print "passei aqui"
        return True     

    except Exception as e:
        print "Deu pau..",e.message_dict
        return e.message

    
def consultar_entidade(request,entidade_id):
    
    registro_entidade = entidade.objects.get(pk=entidade_id)
    
    if (request.method == "POST"):
        formulario = formulario_cadastro_entidade_completo()
    else:
        
        dados = {'cpf_cnpj':registro_entidade.cpf_cnpj,
                 'nome_razao':registro_entidade.nome_razao,
                 'apelido_fantasia':registro_entidade.apelido_fantasia,
                 'tipo_registro':registro_entidade.tipo_registro,
                 'nascimento_fundacao':registro_entidade.nascimento_fundacao
                }
        
        formulario = formulario_cadastro_entidade_completo(dados)
        
        
        
    return render_to_response("consultar_entidade.html",{'dados':registro_entidade,'formulario':formulario,'erro':False},context_instance=RequestContext(request))


def construir_objeto_localizacao(formulario, registro_entidade):
    
    codigo_postal = remover_simbolos(formulario.cleaned_data['cep'])                
    registro_endereco = endereco.objects.get(cep=codigo_postal)
    
    registro = localizacao(
        #entidade    = registro_entidade,
        cep      = registro_endereco,
        numero      = str(formulario.cleaned_data['numero_endereco']),
        complemento = formulario.cleaned_data['complemento'].upper(),
    )
    return registro

def construir_objeto_contato(formulario, registro_entidade):
    registro = contato(
        #entidade = registro_entidade,#entidade.objects.get(pk=registro_entidade.id),
        nome_contato = registro_entidade.nome_razao,
        tipo_contato = formulario.cleaned_data['tipo_contato'],
        numero       = remover_simbolos(formulario.cleaned_data['numero_contato']),
        cargo_setor  = formulario.cleaned_data['cargo_setor'],
        email        = formulario.cleaned_data['email'],
    )      
    return registro


def construir_objeto_entidade(formulario):
    registro = entidade()
    registro.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
    registro.nome_razao = formulario.cleaned_data['nome_razao'].upper()
    registro.apelido_fantasia = formulario.cleaned_data['apelido_fantasia'].upper()
    registro.tipo_registro = formulario.cleaned_data['tipo_registro']
    registro.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
    return registro

def validar_registro(registro):
    try:
        registro.clean()
        return True        
        
    except IntegrityError as excecao:
        if "cpf_cnpj" in excecao.message:
            msg = "Erro! cpf ou cnpj já existe no cadastro!"
        
        else:
            msg = excecao.message
        
        return msg
                    
    

def cadastro_entidades(request):  
    
    dados = entidade.objects.all()
    #if 'elevar_indice_categoria' in request.POST:  
    
    if (request.method == "POST"):
                
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)        
        codigo_postal = remover_simbolos(formulario['cep'].value())
                
        if formulario.is_valid():
            msg = ""
            
            registro_entidade = construir_objeto_entidade(formulario)
            if validar_registro(registro_entidade) == True:                
                #registro_entidade.save()
                
                registro_contato = construir_objeto_contato(formulario, registro_entidade)
                if validar_registro(registro_contato):
                    #registro_contato.save()        
                            
                    registro_localizacao = construir_objeto_localizacao(formulario, registro_entidade)
                    if validar_registro(registro_localizacao):
                        registro_entidade.save()
                        registro_localizacao.entidade = registro_entidade
                        registro_localizacao.save()
                        registro_contato.entidade = registro_entidade
                        registro_contato.save()  
                
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
                
                formulario = formulario_cadastro_entidade_completo()
                
            else:
                messages.add_message(request, messages.SUCCESS, msg)
                
        
        else:
            
            msg = ""            
            for campo in formulario:
                erros = campo.errors.as_data()
                
                
                if erros != []:
                    
                    
                    erro = erros[0][0]
                    
                    print erro
                    
                    if 'email' in erro:
                        msg = "Erro! "+unicode(erro)
                    
                    elif 'data' in erro:          
                        msg = "Erro! "+unicode(erro)
                    
                    else:
                        msg = campo.label+" "+erro
                    
                        
                        
                    messages.add_message(request, messages.SUCCESS, msg)
                    break
            return render_to_response("cadastro_entidades.html",{'dados':dados,'formulario':formulario,'erro':True},context_instance=RequestContext(request))
    
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contato  = form_adicionar_contato()
    
    return render_to_response("cadastro_entidades.html",{'dados':dados,'formulario':formulario,'erro':False},context_instance=RequestContext(request))







    
    
    """
    if request.POST:
        form = formulario_cadastro_entidade_completo(request.POST, request.FILES)
        if form.is_valid():
            print "deu certo!"

    else:
        form = formulario_cadastro_entidade_completo()

    #return render(request, 'contact/form.html', {'form':form})
    
    return render_to_response("cadastro_entidades.html",{'formulario':form},context_instance=RequestContext(request))
    """

def verificar_erros_formulario(formulario):
    msg = ""            
    for campo in formulario:
        erros = campo.errors.as_data()
                
        if erros != []:
            
            erro = erros[0][0]
                        
            if 'email' in erro:
                msg = "Erro! "+unicode(erro)
            
            elif 'data' in erro:          
                msg = "Erro! "+unicode(erro)
            
            else:
                msg = campo.label+" "+unicode(erro)
            
            return msg
    
          

def consultar_cep(request,codigo_postal):
    
    if request.is_ajax():
        codigo_postal = codigo_postal.replace(".","")
        codigo_postal = codigo_postal.replace("-","")
        
        resultado = endereco.objects.filter(cep=codigo_postal)
               
        if resultado.count() == 0:
            resultado = consultar_codigo_postal(codigo_postal)
            
            
            if resultado != None:
                resultado[0] = formatar_codificacao(resultado[0])
                resultado[1] = formatar_codificacao(resultado[1])
                resultado[2] = formatar_codificacao(resultado[2])
                                                                  
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
                
                try:                    
                    registro_endereco.save()

                except Exception as excecao:
                    print "deu problema",excecao.message
                    
            else:
                resultado = ["","","","","",""]
            
        else:
            registro_endereco = resultado[0]
            registro_bairro = bairro.objects.get(id=registro_endereco.bairro_id)
            registro_cidade = registro_bairro.municipio 
            registro_estado = registro_cidade.estado    
            resultado = [registro_endereco.nome,registro_bairro.nome,registro_cidade.nome,registro_estado.sigla,registro_cidade.codigo_ibge,registro_estado.pais.nome]
            #print "Deu certo: ",resultado
        
        
        #print "Verfique o resultado: ",resultado
        data = json.dumps(resultado)
        return HttpResponse(data, content_type='application/json')
    
    else:
        raise Http404




def adicionar_entidade(request):
    
    dados = entidade.objects.all()
    
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
            
            return render_to_response("adicionar_entidade.html",{'dados':dados,'formulario':formulario},context_instance=RequestContext(request))
    
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contato  = form_adicionar_contato()
        
    return render_to_response("adicionar_entidade.html",{'dados':dados,'formulario':formulario},context_instance=RequestContext(request))
        
    #return render_to_response("adicionar_entidade.html",{'formulario_entidade':formulario_entidade,'formulario_contato':formulario_contato},context_instance=RequestContext(request))   
        
