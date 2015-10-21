'''
Created on 29 de set de 2015

@author: Diego
'''

def formatar_codificacao(texto):
    texto = u''+unicode(texto, "latin-1")   
    texto = texto.upper()
    return texto 

def remover_simbolos(texto):
    texto = texto.replace(".","")
    texto = texto.replace(",","")
    texto = texto.replace("-","")
    return texto