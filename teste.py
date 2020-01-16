'''from conexao import Requisicao
requisicao = Requisicao('url')
velocidade = requisicao.speed()
print(velocidade[0])'''
import csv
lista = []
down = []
up = []
ping = []
contratado_down = 30
contratado_up = 15
with open('log.csv', 'r', newline='', encoding="ISO-8859-1") as csvfile:
    ler = csv.reader(csvfile)
    for i in ler:
        lista.append(i[3])

for i in range(len(lista)):
    down.append(int(lista[i][12:14]))
    up.append(int(lista[i][31:33]))
    ping.append(int(lista[i][48]))

media_down = sum(down) / len(down)
media_down = round(media_down)
print(media_down)
porcento_down = (media_down/contratado_down) * 100
print(porcento_down)
media_up = sum(up) / len(up)
porcento_up = (media_up/contratado_up) * 100
print(porcento_up)
media_ping = sum(ping) / len(ping)
print(media_ping)
