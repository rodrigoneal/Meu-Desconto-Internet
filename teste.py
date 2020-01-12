import csv
lista = []
dados = []
datas = []
path = 'log.csv'
with open(path, 'r', newline='') as csvfile:
    escrever = csv.reader(csvfile)
    for i in escrever:
        lista.append(i)
for i in range(len(lista)):
    dados.append(lista[i][0][:10])
dados = sorted(set(dados))
selecionado = dados[1]
for i in range(len(lista)):
    if selecionado == lista[i][0][:10]:
        print(lista[i][2])

