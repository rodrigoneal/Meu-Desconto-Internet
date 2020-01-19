#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import time
import requests
from datetime import datetime
from pushbullet import Pushbullet
import DB


def pushbullet(*mensagem):
    for i in mensagem:
        envio = str(mensagem)
    try:
        token = 'o.pefpmkVrXSzUGUAKpnYjgArR5STuus9h'
        pb = Pushbullet(token)
        celular = pb.devices[0]
        pb.push_note("A internet Acabou de se recuperar", envio, celular)
    except:
        raise print('Falha ao enviar mensagem')


def getHora():
    """
    :return a hora atual já convertida para o ABNT

    """
    now = datetime.now()
    dia_hora = now.strftime("%d/%m/%Y, %H:%M:%S")
    dia = dia_hora.split(',')[0]
    hora = dia_hora.split(',')[1].lstrip()
    return dia, hora


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

    # Começo arquivos de inicialização
    def __init__(self, url):
        self.url = url

    def conectar(self):
        """
        Faz um tentativa de requisião ao URL que foi passado no chamado da classe:

        :return 1 para requisição positiva e 2 quando não consegue se conectar

        :return hora dessa requisição

        """
        dia = getHora()[0]
        hora = getHora()[1]
        try:
            requests.get(self.url, timeout=5)

            return 1, dia, hora
        except:
            return 2, dia, hora

    def diferenca(self, lista):
        """
        Recebe  uma lista de requisição, pega a primeira e a ultima tentativa de conexão. Muda o tempo para String
        e calcula o tempo que ficou sem internet.

        :return a hora que caiu e a hora que voltou mais e o calculo do tempo que ficou sem internet em minutos.

        """
        queda_data = str(lista[0][1])  # Data que a internet caiu
        queda_hora = str(lista[0][2])  # Hora que a internet caiu

        volta_data = str(lista[-1][1])  # Data que a internet voltou
        volta_hora = str(lista[-1][2])  # Data que a internet voltou

        queda_convertida = f'{queda_data} {queda_hora}'
        volta_convertida = f'{volta_data} {volta_hora}'

        fmt = '%d/%m/%Y %H:%M:%S'
        d1 = datetime.strptime(queda_convertida, fmt)
        d2 = datetime.strptime(volta_convertida, fmt)
        tempooff = (d2 - d1)
        tempooff = str(tempooff)
        return queda_hora, queda_data, volta_hora, volta_data, tempooff

    def salvar(self, *args, path):
        """
        Salva um arquivo CSV no caminho(path) informado

        """

        with open(path, 'a', newline='', encoding="ISO-8859-1") as csvfile:
            escrever = csv.writer(csvfile)
            escrever.writerow(args)

    # Começo arquivos de inicialização
    # Começo dos metodos do menu
    def menu(self):
        """
        Criação de um menu para simplificação na hora de mostrar a informação
        :return: a opção que o usuario escolhe
        """
        print('*_*-' * 5, 'Menu', '*_*-' * 5)
        print('Digite 1: Para Relatório por dia')
        print('Digite 2: Para Relatório por mes')
        print('Digite 3: Para Relatório de descontos')
        print('Digite 4: Para Qualidade da sua internet')
        print('Digite 5: Para Analise da internet')
        print('Digite 6: Para Fechar o programa')
        escolha = int(input(': '))
        return escolha

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

    def media_internet(self, vdown, vup):  # Já em DB

        somadown = []
        somaup = []
        somaping = []
        contratado_down = float(input('Qual a velocidade de Download contratada em MB: '))
        contratado_up = float(input('Qual a velocidade de Upload contratada em MB: '))
        down = DB.select('down')
        up = DB.select('up')
        ping = DB.select('ping')
        for i in down:
            for v in i:
                somadown.append(v)
        for i in up:
            for v in i:
                somaup.append(v)
        for i in ping:
            for v in i:
                somaping.append(v)

        mediadown = sum(somadown) / len(somadown)
        mediaup = sum(somaup) / len(somaup)
        mediaping = sum(somaping) / len(somaping)
        porcento_down = (mediadown / contratado_down) * 100
        porcento_up = (mediaup / contratado_up) * 100
        print(f'A sua media de Download foi de {mediadown:.2f} MB')
        print(f'A sua media de Upload foi de {mediaup:.2f} MB')
        print(f'A sua media de ping foi de {mediaping:.2f} ms')
        print("")
        print(f'Com isso você está recebendo {porcento_down:.2f}% da sua internet contratada para Download', end='')
        print(f' e {porcento_up:.2f}% da sua internet contratada para Upload')
        print(f'Seu maior ping foi {max(somaping)}ms e o menor foi {min(somaping)}ms')

    # Fim dos metodos do menu

    # Começo dos arquivos de analise

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
            down = (round(res["download"] / 1024 / 1024))
            up = (round(res["upload"] / 1024 / 1024))
            ping = (round(res["ping"]))
            return down, up, ping
        except:
            pass

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
