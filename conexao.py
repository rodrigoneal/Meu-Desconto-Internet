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

    def salvar(self, save, path):
        """
        Salva um arquivo CSV no caminho(path) informado

        """
        with open(path, 'a', newline='') as csvfile:
            escrever = csv.writer(csvfile)
            escrever.writerow(save)

    def diferenca(self, lista,cidade):
        """
        Recebe  uma lista de requisição, pega a primeira e a ultima tentativa de conexão. Muda o tempo para String
        e calcula o tempo que ficou sem internet.

        :return a hora que caiu e a hora que voltou mais e o calculo do tempo que ficou sem internet em minutos.

        """
        s = str(lista[0][1]).replace(',', '')
        t = str(lista[-1][1]).replace(',', '')
        print(s)
        print(t)
        fmt = '%d/%m/%Y %H:%M:%S'
        d1 = datetime.strptime(s, fmt)
        d2 = datetime.strptime(t, fmt)
        valor = (d2 - d1)
        velocidade = self.speed()
        clima = getClima(cidade)
        return s, t, valor, velocidade, clima

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
            down = ('Download: {:.2f} Kb/s'.format(res["download"] / 1024))
            up = ('Upload: {:.2f} Kb/s'.format(round(res["upload"] / 1024)))
            ping = ('Ping: {}'.format(res["ping"]))
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
        with open(path, 'r', newline='') as csvfile:
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
            if hora > 23:
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
        return f'Você ficou {dia} dias e  {data} sem internet esse mês e o seu desconto na internet deve ser de R${desconto} \n'
