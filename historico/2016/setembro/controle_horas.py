from datetime import datetime, date, time

def carregar_arquivos():
    import glob
    arquivos = []
    for arquivo in glob.glob('*.txt'):
        arquivos.append(arquivo)
    return arquivos

def processar_arquivo(arquivo):
    import re
    arquivo = open(arquivo)
    pattern = re.compile("(\[.*\])(.*)")

    data_inicio        = None
    duracao_total      = None
    intervalo_anterior = None
    
    for line in arquivo:
        resultado = pattern.match(line)
        if resultado and "/arquivos_estaticos/" not in line and "u'" not in line:
            data = processar_data(resultado.group(1))#+" ======> "+resultado.group(2)
            if data_inicio == None:
                data_inicio = data
                intervalo_anterior = data
                duracao_total = data-data
                #print "(",duracao_total,")"
                continue

            #print "olha o intervalo anterior: ",intervalo_anterior
            if data != None:
                intervalo = data - intervalo_anterior

                minutos_intervalo_maximo = 50

                if intervalo.seconds > minutos_intervalo_maximo*60:
                    #print "(",intervalo,") > INTERVALO"
                    pass
                else:
                    #print "(+",intervalo,")"
                    duracao_total = duracao_total + intervalo

                intervalo_anterior = data

    return duracao_total
            
def processar_data(linha):
    
    linha = linha.replace("[","")
    linha = linha.replace("]","")
    campos = linha.split(" ")

    try:
        campos[0] = converter_data(campos[0])
        data_campos = campos[0].split("/")
        hora_campos = campos[1].split(":")

        data = date(int(data_campos[2]), int(data_campos[1]), int(data_campos[0]))
        hora = time(int(hora_campos[0]),int(hora_campos[1]),int(hora_campos[2]))
        data_completa = datetime.combine(data, hora)
        return data_completa

    except:
        return None
    #print data_completa,


def converter_data(texto):
    if "Aug" in texto:
        return texto.replace("Aug","08")
    
    elif "Sep" in texto:
        return texto.replace("Sep","09")
        

def calcular_horas():
    arquivos = carregar_arquivos()
    horas_totais = None
    for item in arquivos:
        dia = item[:item.find(".")]
        horas_dia = processar_arquivo(item)
        #print "\n\n"

        if horas_totais == None:
            horas_totais = horas_dia

        horas_totais = horas_totais + horas_dia
        print dia,"-",horas_dia

    print "HORAS TOTAIS TRABALHADAS:",horas_totais
    return horas_totais


if __name__=="__main__":
    calcular_horas()
    raw_input("Pressione Enter para prosseguir..")


