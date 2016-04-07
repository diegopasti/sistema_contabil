# -*- encoding: utf-8 -*-
import cgi
import urllib

def consultar_cep(cep):
    #from entidade.models import endereco
    #print "tentando fazer uma consultinha"
    #print endereco.objects.get(cep=cep)
    return consultar_remota(cep)
    
def consultar_remota(cep):

    cep = cep.replace(".","")
    cep = cep.replace("-","")
    cep_busca   = cep;  
        
    url         = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + cep_busca + "&formato=query_string"  
    pagina      = urllib.urlopen(url)  
    conteudo    = pagina.read();  
    resultado   = cgi.parse_qs(conteudo);
    
    if resultado['resultado'][0] == '1':
        #print "Endereco com cidade de CEP unico: "  
        endereco = resultado['tipo_logradouro'][0].upper()+" "+resultado['logradouro'][0].upper()
        bairro = resultado['bairro'][0].upper()
        cidade = resultado['cidade'][0].upper()
        uf     = resultado['uf'][0].upper()
        resultado = [endereco,bairro,cidade,uf,]
        
    elif resultado['resultado'][0] == '2':
        #print "Endereco com cidade de CEP unico: "  
        cidade = resultado['cidade'][0].upper()  
        uf     = resultado['uf'][0].upper() 
        resultado = ["","",cidade,uf,]
    else:  
        resultado = None
        
    return resultado
