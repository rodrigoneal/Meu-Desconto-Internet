import csv
from locale import setlocale, LC_ALL
from calendar import month_name
path = 'log.csv'
mes = []
lista = []
hora = []
minuto = []
segundo = []
setlocale(LC_ALL, 'pt-BR')
with open(path, 'r', newline='') as csvfile:
    escrever = csv.reader(csvfile)
    indice = escrever

    for i in indice:
        try:
            lista.append(i)
            mes.append(i[0][3:5])
        except:
            IndexError
mes = sorted(set(mes))
for i in mes:
    print(f'Digite {mes.index(i)+1} para o mes de {month_name[int(i)].capitalize()}')

escolha = int(input(': ')) - 1
print(escolha)
for i in range(len(lista)):
    try:
        if lista[i][0][3:5] == mes[escolha]:
            get = (lista[i][2])
            get = get.split(':')
            segundo.append(int(get[2]))
            minuto.append(int(get[1]))
            hora.append(int(get[0]))
    except:
        IndexError
segundo = sum(segundo)
minuto = sum(minuto)
hora = sum(hora)
dia = 0
cont = 0
while cont < len(lista):
    if segundo > 59:
        minuto += 1
        segundo -= 59
    if minuto > 59:
        hora += 1
        minuto -= 59
    if hora > 23:
        dia += 1
        hora -= 23
        dia += 1
    cont += 1
print(f'O tempo gasto no {mes} foi de {hora}:{minuto}:{segundo}')
