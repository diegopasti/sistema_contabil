'''
Created on 1 de abr de 2016

@author: Win7
'''
from django.shortcuts import render_to_response


def cadastro_protocolo(request):
    return render_to_response("protocolo/cadastro_protocolo.html")