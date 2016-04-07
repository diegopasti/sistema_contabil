from django.http.response import HttpResponse


def teste(request):
    print "vim aqui?"
    from endereco.service import consultar_cep
    resultado = consultar_cep("29018250")
    
    return HttpResponse(resultado)