# -*- encoding: utf-8 -*-

import StringIO
from cgi import escape
from decimal import Decimal
import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import Http404, HttpResponseRedirect
from django.http.response import HttpResponse  # , Http404
from django.shortcuts import render_to_response  # , redirect
from django.template.context import RequestContext

from entidade.formularios import formulario_cadastro_entidade_completo, formulario_emitir_protocolo  # , formulario_adicionar_item_protocolo
from entidade.models import Endereco, Estado, Municipio, Bairro, Logradouro, localizacao_simples  # localizacao 
from entidade.models import entidade, contato
from entidade.service import consultar_estado, consultar_codigo_postal_viacep  # consultar_codigo_postal_default
from entidade.utilitarios import formatar_codificacao
from entidade.utilitarios import remover_simbolos  # formatar_codificacao, 
from protocolo.models import item_protocolo


#import os
#from django.core.exceptions import ValidationError
#from sistema_contabil import settings
#from util.internet import consultar_codigo_postal
def index(request):
    dados = entidade.objects.all()
    if len(dados) != 0:
        return render_to_response("index.html")
    else:
        return HttpResponseRedirect('/cadastrar_empresa')   
        

def buscar_fontes(request):
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



def buscar_entidades(request):
    print "to vindo aqui"
    resultado = entidade.objects.all()
    
    results = []

    for item in resultado:
        
    
        dado = {}
        dado['cliente'] = item.nome_razao
        results.append(dado)
        
    texto = json.dumps(results)

    return HttpResponse(texto)


def formatar_cep(cep):
    novo_cep = cep[:2]+"."+cep[2:5]+"-"+cep[5:]    
    return novo_cep

def formatar_cpf(cpf):
    novo_cpf = cpf[:3]+"."+cpf[3:6]+"."+cpf[6:9]+"-"+cpf[9:]
    return novo_cpf

def formatar_cpfcnpj(codigo):
    if len(codigo) == 11:
        return formatar_cpf(codigo)
    else:
        return formatar_cnpj(codigo)

def formatar_cnpj(cnpj):
    novo_cnpj = cnpj[:2]+"."+cnpj[2:5]+"."+cnpj[5:8]+"/"+cnpj[8:12]+"-"+cnpj[12:]
    return novo_cnpj

def construir_endereco(localizacao):
    comp = localizacao.complemento
    num  = localizacao.numero
    rua = Logradouro.objects.get(pk=localizacao.cep_id)
    Bairro = Bairro.objects.get(pk=rua.bairro_id)
    Cidade = Municipio.objects.get(pk=Bairro.municipio_id)
    Estado = Estado.objects.get(pk=Cidade.estado_id)
    
    
    endereco_completo = rua.nome+", "+num+", "+comp+", "+Bairro.nome+", "+Cidade.nome+", "+Estado.nome+" - "+formatar_cep(rua.cep)
    return endereco_completo


def gerar_pdf(request):
    from django.template import Context# loader,, Template
    #from xhtml2pdf import pisa
   
    parametros = {'emissor':"Digitar Contabilidade",
                          'destinatario':"HELDER PASTI",
                          'endereco_destinatario':"Rua demósthenes Nunes Vieira, 60, Alto Lage, Cariacica - ES",
                          'endereco_emissor':"Reta da Penha, Vitória - ES",
                          'codigo_protocolo':"P102",
                          'documentos':[
                                            ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                                            ["8","EMISSÃO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                                            ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                                        ],
                          'formulario_protocolo':"Nada por enquanto",
                           'erro':"sem erros tambem"}
    
    c = Context(parametros)#{'message': 'Your message'})
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/novo_protocolo.html', file_object=resp,context=c)
    return result
"""
def link_callback(uri, rel):
    
    #Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    #resources
    
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path
"""    

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
            
            for item in formulario_protocolo.temporarios:                
                print "Olha o iten: ",item
                
            
            nome_cliente = formulario_protocolo['entidade_destinatario'].value().upper()
            id_cliente = int(nome_cliente[:nome_cliente.index("-")])
            
            cliente = entidade.objects.get(pk=id_cliente)
            cliente.cpf_cnpj = formatar_cpfcnpj(cliente.cpf_cnpj)
            
            empresa = entidade.objects.get(pk=1)
            empresa.cpf_cnpj = formatar_cpfcnpj(empresa.cpf_cnpj)
            
            ""
            endereco_cliente = "RUA TESTE.. TO ACERTANDO AS COISAS NO NOVO MODULO DE ENDERECO"#construir_endereco(localizacao.objects.get(entidade_id=cliente.id))
            endereco_emissor = "RUA TESTE.. TO ACERTANDO AS COISAS NO NOVO MODULO DE ENDERECO"#construir_endereco(localizacao.objects.get(entidade_id=empresa.id))
            
            
            pagina = "protocolo.html"
            parametros = {'emissor':empresa,
                          'destinatario':cliente,
                          'endereco_destinatario':endereco_cliente,
                          'endereco_emissor':endereco_emissor,
                           'documentos':formulario_protocolo.temporarios,
                          'formulario_protocolo':formulario_protocolo,
                           'erro':erro}
            
            
            from django.template import loader,Context#, Template
            from xhtml2pdf import pisa
           
            
            pagina = loader.get_template('novo_protocolo.html')
            
            c = Context(parametros)#{'message': 'Your message'})
            html = pagina.render(c)
            
            from django_xhtml2pdf.utils import generate_pdf
            resp = HttpResponse(content_type='application/pdf')
            result = generate_pdf('novo_protocolo.html', file_object=resp,context=c)
            return result
            
            
            resp = HttpResponse(content_type='application/pdf')
            result = generate_pdf(html)#, file_object=resp)
            
            #print "Olha o result:", result
            
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
            #return result.getvalue()
        
            
            """
            return render_to_response("protocolo.html",{
                                        'emissor':empresa,
                                        'destinatario':cliente,
                                        'endereco_destinatario':endereco_cliente,
                                        'endereco_emissor':endereco_emissor,
                                        'documentos':formulario_protocolo.temporarios,
                                        'formulario_protocolo':formulario_protocolo,
                                        'erro':erro},
                                      
                                      context_instance=RequestContext(request))
            """
            
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
    
    """
    if (request.method == "POST"):
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST, request.FILES)
        
        print "olha antes o que tem na data: ",formulario_protocolo.data_emissao
        
        formulario_itens     = formulario_adicionar_item_protocolo(request.POST, request.FILES)
        
        if 'adicionar_item' in request.POST:
            
            if formulario_itens.is_valid():
                documento  = formulario_itens['documento'].value().upper()
                referencia = formulario_itens['referencia'].value()
                vencimento = formulario_itens['vencimento'].value()
                valor      = formulario_itens['valor'].value()
                complemento      = formulario_itens['complemento'].value().upper()
                
                item            = item_protocolo()
                item.documento  = formulario_itens['documento'].value().upper()
                item.complemento= formulario_itens['complemento'].value().upper()
                item.referencia = formulario_itens['referencia'].value()
                item.vencimento = formulario_itens['vencimento'].value()
                item.valor      = formulario_itens['valor'].value()
                
                formulario_itens  = formulario_adicionar_item_protocolo()
                
                print "olha o que tem na data: ",formulario_protocolo.data_emissao
                #itens_temporarios = [documento,referencia,vencimento,valor]
                                
                print "Ve o que tem nos temporarios antes de validar_registro: ",formulario_itens.temporarios
                formulario_itens.temporarios.append(item)
                                
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
        
    elif (request.method == "GET"):
        formulario_emitir_protocolo.temporarios = []
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_itens     = formulario_adicionar_item_protocolo()
        formulario_itens.temporarios = []   
        print "Tem alguma coisa pra mostrar: ",formulario_itens.temporarios
        
        
        
    elif request.is_ajax():
        formulario_itens.temporarios.remove(formulario_itens.temporarios[numero_item])
        print "apaguei, ve o que sobrou: ",formulario_itens.temporarios
        
    
    return render_to_response("emitir_protocolo.html",{'dados':formulario_itens.temporarios,'formulario_protocolo':formulario_protocolo,'formulario_itens':formulario_itens,'erro':erro},context_instance=RequestContext(request))
    """

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


def construir_objeto_localizacao(formulario):

    registro = localizacao_simples(
        cep = remover_simbolos(formulario['cep'].value()),
        numero      = str(formulario.cleaned_data['numero_endereco']),
        complemento = formulario.cleaned_data['complemento'].upper(),
        
        logradouro  = formulario.cleaned_data['endereco'].upper(),
        bairro      = formulario.cleaned_data['bairro'].upper(),
        codigo_ibge = formulario.cleaned_data['codigo_municipio'].upper(),
        municipio   = formulario.cleaned_data['municipio'].upper(),
        estado       = formulario.cleaned_data['estado'].upper() 
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
    msg = ""
    try:
        registro.full_clean()
        msg = "SUCESSO"
    
    except ValidationError as excecao:   
        msg = "Erro! "+excecao.message
        
    except IntegrityError as excecao:
        if "cpf_cnpj" in excecao.message:
            msg = "Erro! cpf ou cnpj já existe no cadastro!"
        
        else:
            msg = excecao.message

        return msg,""
    
    finally:
        return False,""
                    
    

def cadastro_entidades(request):  
    
    dados = entidade.objects.all()
    if len(dados) != 0:
    
    
    
        if (request.method == "POST"):
                    
            formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)        
            codigo_postal = remover_simbolos(formulario['cep'].value())
            erro = False
            if formulario.is_valid():
                msg = ""
                
                registro_entidade = construir_objeto_entidade(formulario)
                registro_contato = construir_objeto_contato(formulario, registro_entidade)
                registro_localizacao = construir_objeto_localizacao(formulario)
                
                print "Olha as validacoes: ",registro_entidade,"-",registro_contato,"-",registro_localizacao
                
                if validar_registro(registro_entidade) and validar_registro(registro_contato) and validar_registro(registro_localizacao):
                    print "Tudo certo.. podemos salvar"
                    registro_entidade.save()
                    registro_localizacao.entidade = registro_entidade
                    registro_localizacao.save()
                    registro_contato.entidade = registro_entidade
                    registro_contato.save()  
                    messages.add_message(request, messages.SUCCESS, "Registro salvo com sucesso!")
                    
                else:
                    print "Problema de validacao.. tem que reapresentar o formulario.."
                    messages.add_message(request, messages.SUCCESS, "Problemas com alguma informação!")
                
                
                """
                if validar_registro(registro_entidade) == True:   
                    print "Entidade salva com Sucesso!"             
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
                    
                            #Endereco = formulario.cleaned_data['Endereco']
                    
                        print "cheguei a concluir isso?"
                        bairro = formulario.cleaned_data['bairro']
                        
                        municipio = formulario.cleaned_data['Municipio']
                        codigo_municipio = remover_simbolos(formulario.cleaned_data['codigo_municipio'])
                        Estado = formulario.cleaned_data['Estado']
                        
                        Pais = formulario.cleaned_data['Pais']
                        tipo_contato = formulario.cleaned_data['tipo_contato']
                        numero_contato = remover_simbolos(formulario.cleaned_data['numero_contato'])
                        cargo_setor = formulario.cleaned_data['cargo_setor']
                        email = formulario.cleaned_data['email']
                    
                        messages.add_message(request, messages.SUCCESS, "Registro salvo com sucesso!")
                        
                        formulario = formulario_cadastro_entidade_completo()
                    
                else:
                    print 'deu erro na entidade'
                    messages.add_message(request, messages.SUCCESS, msg)
                """   
            
            else:
                print "Falha na validacao dos campos"
                msg = ""            
                for campo in formulario:
                    erros = campo.errors.as_data()
                    
                    if erros != []:
                        
                        
                        erro = erros[0][0]
                        
                        print "olha o erro:",campo.label+" "+erro
                        
                        if 'email' in erro:
                            msg = "Erro! "+unicode(erro)
                        
                        elif 'data' in erro:          
                            msg = "Erro! "+unicode(erro)
                        
                        else:
                            msg = campo.label+" "+erro
                            
                        messages.add_message(request, messages.SUCCESS, msg)
                        break
                return render_to_response("entidade/cadastro_entidades.html",{'dados':dados,'formulario':formulario,'erro':True},context_instance=RequestContext(request))
        
        else:
            formulario = formulario_cadastro_entidade_completo()
            #formulario_contato  = form_adicionar_contato()
    
    else:
        return HttpResponseRedirect('/cadastrar_empresa')
    
    return render_to_response("entidade/cadastro_entidades.html",{'dados':dados,'formulario':formulario,'erro':False},context_instance=RequestContext(request))







    
    
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
    from entidade.models import Logradouro
    if request.is_ajax():
        
        codigo_postal = codigo_postal.replace(".","")
        codigo_postal = codigo_postal.replace("-","")
        
        resultado = Logradouro.objects.filter(cep=codigo_postal)
               
        if True: #resultado.count() == 0:
            print "Nao achei na base de dados"
            resultado = consultar_codigo_postal_viacep(codigo_postal)
            #return HttpResponse(resultado, content_type='application/json')
            #resultado = [resultado['logradouro'],resultado['bairro'],resultado['municipio'],resultado['estado'],resultado['codigo_municipio'],resultado['pais']]
            
            """
            if resultado != None:
                resultado[0] = formatar_codificacao(resultado[0])
                resultado[1] = formatar_codificacao(resultado[1])
                resultado[2] = formatar_codificacao(resultado[2])
                                                                  
                registro_estado    = Estado.objects.get(sigla=resultado[3])            
                registro_pais      = registro_estado.Pais.nome
                registro_municipio = Municipio.objects.select_related().get(Estado=registro_estado,nome=resultado[2])
                codigo_municipal   = registro_municipio.codigo_ibge
                resultado.append(codigo_municipal)
                resultado.append(registro_pais)
                
                print "ate aqui eu consegui.."          
                registro_bairro = Bairro.objects.select_related().get(municipio=registro_municipio,nome=resultado[1])
                
                print "achei o bairro?"                       
                registro_endereco = Endereco(
                                     cep = codigo_postal,
                                     Bairro = registro_bairro,
                                     nome = resultado[0]
                                    )
                
                try:             
                    print "salvei um novo Endereco"       
                    registro_endereco.save()

                except Exception as excecao:
                    print "deu problema",excecao.message
                    
            else:
                resultado = ["","","","","",""]
            """
            
        else:
            print "Achei na base de dados"
            registro_endereco = resultado[0]
            registro_bairro = Bairro.objects.get(id=registro_endereco.bairro_id)
            registro_cidade = registro_bairro.municipio 
            registro_estado = registro_cidade.estado    
            resultado = [registro_endereco.nome,registro_bairro.nome,registro_cidade.nome,registro_estado.sigla,registro_cidade.codigo_ibge,registro_estado.pais.nome]
            print "Deu certo: ",resultado
        
        
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
                cep_id = Logradouro.objects.filter(cep=codigo_postal)
                print "Cep ID: ",cep_id
                
                """
                registro_localizacao = localizacao(
                    cep_id      = cep_id,
                    numero      = formulario.cleaned_data['numero_endereco'],
                    complemento = formulario.cleaned_data['complemento'],
                    
                    )
                """
            
                #Endereco = formulario.cleaned_data['Endereco']
                
                bairro = formulario.cleaned_data['bairro']
                
                Municipio = formulario.cleaned_data['Municipio']
                codigo_municipio = remover_simbolos(formulario.cleaned_data['codigo_municipio'])
                Estado = formulario.cleaned_data['Estado']
                
                Pais = formulario.cleaned_data['Pais']
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
        
