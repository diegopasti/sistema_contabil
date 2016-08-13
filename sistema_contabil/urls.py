"""sistema_contabil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [

    url(r'^$', "entidade.views.index"),
    
    url(r'^cadastrar_empresa$', "nucleo.views.cadastrar_empresa"),
    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'teste/$', "endereco.views.teste"),
    
    url(r'^index/$', "entidade.views.index"),
    
    url(r'^gerar_pdf/$', "protocolo.views.gerar_pdf"),
    url(r'^protocolo/$', "protocolo.views.cadastro_protocolo"),
    url(r'^protocolo/get_detalhes_protocolo/(?P<protocolo_id>\d+)/$', "protocolo.views.get_detalhes_protocolo"),
    url(r'^protocolo/visualizar/(?P<protocolo_id>\d+)/$', "protocolo.views.visualizar_protocolo"),
    
    url(r'^protocolo/emitir_protocolo/$', "protocolo.views.novo_emitir_protocolo"),
    url(r'^protocolo/emitir_protocolo/(?P<operador>\w+)/$', "protocolo.views.emitir_protocolo_identificado"),
    url(r'^emitir_protocolo/excluir/(?P<numero_item>\d+)/$', "protocolo.views.emitir_protocolo"),

    url(r'^preferencias/protocolo/documentos/$', "protocolo.views.cadastro_documentos"),
    url(r'^protocolo/documento/(?P<id>\d+)/$', "protocolo.views.get_documento"),
	url(r'^protocolo/documento/excluir/(?P<id>\d+)/$', "protocolo.views.excluir_documento"),
    url(r'^api/protocolo/salvar$', "protocolo.views.salvar_protocolo"),

    url(r'^consultar_cep/(?P<codigo_postal>\d+)/$', "entidade.views.consultar_cep"),

    
    #url(r'^consultar_cep/(?P<cep>\d+\.\d+-\d+)/$', "entidade.views.consultar_cep"),
    url(r'^entidade/$', "entidade.views.cadastro_entidades"),
    url(r'^entidade/adicionar/$', "entidade.views.adicionar_entidade"),
    url(r'^entidade/desativar/(?P<cliente>\d+)/$', "entidade.views.desativar_cliente"),
	url(r'^entidade/visualizar/(?P<id>\d+)/$', "entidade.views.visualizar_entidade"),
    url(r'^api/entidade/lista_clientes/$', "entidade.views.novo_buscar_lista_clientes"),
    
    #url(r'^protocolo/$', "entidade.views.protocolo"),
    
    url(r'^adicionar_entidade/$', "entidade.views.adicionar_entidade"),
    url(r'^consultar_entidade/(?P<entidade_id>\d+)/$',"entidade.views.consultar_entidade"),

    url(r'^preferencias/servicos/$', "servico.views.cadastro_servico"),
    url(r'^api/preferencias/servicos/$', "servico.views.consultar_servicos"),
    url(r'^api/preferencias/novo_servico$', "servico.views.adicionar_servico"),
    url(r'^api/preferencias/alterar_servico/(?P<servico_id>\d+)/$', "servico.views.alterar_servico"),
    url(r'^api/preferencias/excluir_servico/(?P<servico_id>\d+)/$', "servico.views.excluir_servico"),

    url(r'^planos/$', "servico.views.cadastro_planos"),
    url(r'^api/planos/$', "servico.views.consultar_planos"),
    url(r'^api/planos/adicionar$', "servico.views.adicionar_plano"),
    url(r'^api/planos/atualizar', "servico.views.atualizar_plano"),
    url(r'^api/planos/excluir', "servico.views.excluir_plano"),

    url(r'^honorario/$', "honorario.views.honorario_page"),
    url(r'^honorario/contrato$', "honorario.views.contrato_page"),
    url(r'^api/honorario/lista_contratos$', "honorario.views.get_lista_contratos"),


    #url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "preferencias.views.alterar_salario"),
    #url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "preferencias.views.excluir_salario"),
    #url(r'^api/preferencias/salario_vigente/$', "preferencias.views.get_salario_vigente"),

    url(r'^preferencias/$', "preferencias.views.controle_preferencias"),
    url(r'^api/preferencias/salarios$', "preferencias.views.listar_salarios"),
    url(r'^api/preferencias/novo_salario$', "preferencias.views.adicionar_salario"),
    url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "preferencias.views.alterar_salario"),
    url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "preferencias.views.excluir_salario"),
    url(r'^api/preferencias/salario_vigente/$', "preferencias.views.get_salario_vigente"),


    url(r'^api/working/register/$', "nucleo.views.working"),


]
