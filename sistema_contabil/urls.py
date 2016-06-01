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
    
    url(r'^protocolo/emitir_protocolo/$', "protocolo.views.emitir_protocolo",{'numero_item': -1}),
    url(r'^emitir_protocolo/excluir/(?P<numero_item>\d+)/$', "protocolo.views.emitir_protocolo"),
    
    url(r'^consultar_cep/(?P<codigo_postal>\d+)/$', "entidade.views.consultar_cep"),
    url(r'^buscar_entidades/$', "entidade.views.buscar_entidades"),
    
    #url(r'^consultar_cep/(?P<cep>\d+\.\d+-\d+)/$', "entidade.views.consultar_cep"),
    url(r'^cadastro_entidades/$', "entidade.views.cadastro_entidades"),
    
    #url(r'^protocolo/$', "entidade.views.protocolo"),
    
    url(r'^adicionar_entidade/$', "entidade.views.adicionar_entidade"),
    url(r'^consultar_entidade/(?P<entidade_id>\d+)/$',"entidade.views.consultar_entidade"),
]
