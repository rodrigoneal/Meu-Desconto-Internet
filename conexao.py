#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import time
import requests
from datetime import datetime
from pushbullet import Pushbullet


def pushbullet(mensagem):
    for i in mensagem:
        envio = str(mensagem)
    try:
        token = 'o.pefpmkVrXSzUGUAKpnYjgArR5STuus9h'
        pb = Pushbullet(token)
        celular = pb.devices[0]
        push = pb.push_note("A internet Acabou de se recuperar", envio, celular)
    except:
        raise print('Falha ao enviar mensagem')


def getHora():
    """
    :return a hora atual já convertida para o ABNT

    """
    now = datetime.now()
    hora = now.strftime("%d/%m/%Y, %H:%M:%S")
    return hora


def getClima(cidade):
    """
    Pega o clima no Open Weather Map no local do cliente

    :return: Clima quando a internet volta
    """
    try:
        import pyowm
        tempo = pyowm.OWM('61d012c0208ee24cc7fb05093c438767', language='pt')
        local = tempo.weather_at_place(cidade)
        clima = local.get_weather()
        status = clima.get_detailed_status()
        if status == 'nuvens quebradas':
            status = 'Céu limpo com poucas nuvens'
        return status
    except:
        raise print('Erro ao se comunicar com a central do tempo')


class Requisicao:
    """
    Classe que faz desde a requisição até salvar em CSV

    """

    def __init__(self, url):
        self.url = url

    def conectar(self):
        """
        Faz um tentativa de requisião ao URL que foi passado no chamado da classe:

        :return 1 para requisição positiva e 2 quando não consegue se conectar

        :return hora dessa requisição

        """
        hora = getHora()
        try:
            requests.get(self.url, timeout=5)

            return 1, hora
        except:
            return 2, hora

    def salvar(self, *args, path):
        """
        Salva um arquivo CSV no caminho(path) informado

        """

        with open(path, 'a', newline='', encoding="ISO-8859-1") as csvfile:
            escrever = csv.writer(csvfile)
            escrever.writerow(args)

    def diferenca(self, lista):
        """
        Recebe  uma lista de requisição, pega a primeira e a ultima tentativa de conexão. Muda o tempo para String
        e calcula o tempo que ficou sem internet.

        :return a hora que caiu e a hora que voltou mais e o calculo do tempo que ficou sem internet em minutos.

        """
        queda = str(lista[0][1]).replace(',', '')
        volta = str(lista[-1][1]).replace(',', '')
        fmt = '%d/%m/%Y %H:%M:%S'
        d1 = datetime.strptime(queda, fmt)
        d2 = datetime.strptime(volta, fmt)
        tempooff = (d2 - d1)
        tempooff = str(tempooff)
        return queda, volta, tempooff

    def cronometro(self, tempo, mensagem):
        """
        Recebe um tempo e uma mensagem e faz um cronometro com o tempo informado para que não seja feita muitas
        requisições ao mesmo servidor

        """
        cont = tempo - 1
        for i in range(tempo):
            for v in range(59, -1, -1):
                print(mensagem)
                if cont >= 1 and v >= 10:
                    print(f'Nova analise em {cont}:{v} minutos', flush=True)

                elif cont >= 1 and v < 10:
                    print(f'Nova analise em {cont}:{0}{v} Minutos', flush=True)

                elif cont < 1 and v >= 10:
                    print(f'Nova analise em {v} segundos', flush=True)


                elif cont < 1 and v < 10:
                    print(f'Nova analise em {0}{v} segundos', flush=True)

                time.sleep(1)
                os.system('cls')
            cont -= 1

    def speed(self):
        """
        Faz um teste de velocidade após a internet voltar a funcionar

        :return: velocidad de download, upload e o ping
        """

        try:
            import speedtest
            s = speedtest.Speedtest()
            s.get_servers()
            s.get_best_server()
            s.download()
            s.upload()
            res = s.results.dict()
            down = ('Download: {:.0f} MB/s'.format(round(res["download"] / 1024 / 1024)))
            up = ('Upload: {:.0f} MB/s'.format(round(res["upload"] / 1024 / 1024)))
            ping = ('Ping: {:.0f}'.format(res["ping"]))
            return down, up, ping
        except:
            return None

    def desconto(self):
        """
        Varre o registro log.csv e faz um calculo do tempo que ficou sem internet

        :return: Um print informando a quantidade de dias que ficou sem internet num certo mês e o valor de desconto
        pelo tempo sem internet

        """

        lista = []
        hora = []
        minuto = []
        segundo = []
        path = 'log.csv'
        with open(path, 'r', newline='', encoding="ISO-8859-1") as csvfile:
            escrever = csv.reader(csvfile)
            for i in escrever:
                try:
                    lista.append(i[2])
                except:
                    pass
        for i in lista:
            s = i
            t = s.split(':')
            hora.append(int(t[0]))
            minuto.append(int(t[1]))
            segundo.append(int(t[2]))
        hora = sum(hora)
        minuto = sum(minuto)
        segundo = sum(segundo)
        dia = 0
        getdia = 0
        preco_dia = 0
        cont = 0
        PRECO_HORA = 0.25
        PRECO_MINUTO = PRECO_HORA / 60
        PRECO_SEGUNDO = PRECO_MINUTO / 60

        while cont < len(lista):
            if segundo > 59:
                minuto += 1
                segundo -= 59
            if minuto > 59:
                hora += 1
                minuto -= 59
            if hora >= 23:
                dia += 1
                hora -= 23
                getdia = dia
            cont += 1
            if getdia >= 1:
                preco_dia += 6
                getdia = - 1
        preco_hora = PRECO_HORA * hora
        preco_minuto = PRECO_MINUTO * minuto
        preco_segundo = PRECO_SEGUNDO * segundo
        desconto = preco_dia + preco_hora + preco_minuto + preco_segundo
        desconto = round(desconto, 2)

        desconto = str(desconto)
        desconto = desconto.replace('.', ',')
        s = f'{hora}:{minuto}:{segundo}'
        fmt = '%H:%M:%S'
        d1 = datetime.strptime(s, fmt)
        data = str(d1)[11:]
        print(
            f'Você ficou {dia} dias e {data} sem internet esse mês e o seu desconto na internet deve ser de R${desconto} \n')

    def relatorio_dia(self):
        lista = []
        dados = []
        segundos = []
        minutos = []
        horas = []
        error = []
        path = 'log.csv'
        with open(path, 'r', newline='', encoding="ISO-8859-1") as csvfile:
            escrever = csv.reader(csvfile)
            for i in escrever:
                lista.append(i)
        for i in range(len(lista)):
            dados.append(lista[i][0][:10])
        dados = sorted(set(dados))
        print('Por favor')
        for i in dados:
            error.append(dados.index(i))

            print(f'Digite {dados.index(i) + 1} para relatorio do dia {i}')

        dia = int(input(': ')) - 1
        while True:
            if dia in error:
                selecionado = dados[dia]
                break
            else:
                print('Data Invalida')
                selecionado = int(input('Digite Uma data Valida '))
        for i in range(len(lista)):
            if selecionado == lista[i][0][:10]:
                converter = str(lista[i][2])
                converter = converter.split(':')
                segundos.append(int(converter[2]))
                minutos.append(int(converter[1]))
                horas.append(int(converter[0]))
        segundos = sum(segundos)
        minutos = sum(minutos)
        horas = sum(horas)
        for i in range(len(lista)):
            if segundos >= 60:
                minutos += 1
                segundos -= 60
            if minutos >= 60:
                horas += 1
                minutos -= 60
        s = f'{horas}:{minutos}:{segundos}'
        fmt = '%H:%M:%S'
        d1 = datetime.strptime(s, fmt)
        data = str(d1)[11:]
        print(f'No dia {dados[dia]} você ficou {data} sem internet')

    def menu(self):
        print('*_*-' * 5, 'Menu', '*_*-' * 5)
        print('Digite 1: Para Relatório por dia')
        print('Digite 2: Para Relatório por mes')
        print('Digite 3: Para Relatório de descontos')
        print('Digite 4: Para Qualidade da sua internet')
        print('Digite 5: Para Analise da internet')
        print('Digite 6: Para Fechar o programa')
        escolha = int(input(': '))
        return escolha

    def relatorio_mes(self):

        from calendar import month_name

        path = 'log.csv'
        mes = []
        lista = []
        hora = []
        minuto = []
        segundo = []
        with open(path, 'r', newline='', encoding="ISO-8859-1") as csvfile:
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
            print(f'Digite {mes.index(i) + 1} para o mes de {month_name[int(i)].capitalize()}')

        escolha = int(input(': ')) - 1
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
            cont += 1
        print(f'Em {month_name[escolha + 1]} Você ficou ficou {dia} dias {hora}:{minuto}:{segundo} sem internet')

    def media_internet(self, vdown, vup):
        lista = []
        down = []
        up = []
        ping = []
        contratado_down = vdown
        contratado_up = vup
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
        porcento_down = (media_down / contratado_down) * 100

        media_up = sum(up) / len(up)
        porcento_up = (media_up / contratado_up) * 100

        media_ping = sum(ping) / len(ping)

        print(f'Sua Internet contratada é de {contratado_down} de download e {contratado_up} de upload')
        print(f'A sua média de download foi {media_down} correspondendo à {porcento_down}% da sua velocidade '
              f'contratada')
        print(f'A sua média de Upload foi {media_up} correspondendo à {porcento_up}% da sua velocidade contratada')
        print(f'Sua Média de latencia foi de {media_ping}')
