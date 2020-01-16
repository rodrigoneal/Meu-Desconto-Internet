#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import time

import conexao
from conexao import Requisicao

url = 'https://www.google.com/'
path = 'log.csv'
requisicao = Requisicao(url)
lista = []
cidade = 'Rio de Janeiro'
def sistema():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
if __name__ == '__main__':

    """
    Menu simples
    
    """
    while True:
        selecionar = requisicao.menu()
        if selecionar == 1:
            sistema()
            relatorio_dia = requisicao.relatorio_dia()
            time.sleep(5)
            sistema()
        elif selecionar == 2:
            sistema()
            relatorio_mes = requisicao.relatorio_mes()
            time.sleep(5)
            sistema()
        elif selecionar == 3:
            sistema()
            relatorio_desconto = requisicao.desconto()
            time.sleep(5)
            sistema()
        elif selecionar == 4:
            sistema()
            break
        elif selecionar == 5:
            sys.exit()
        else:
            sistema()
            print('Favor digitar uma opção valida')
            time.sleep(5)
            sistema()





    while True:
        """
        Loop infinito para realizar testes de funcionamento da intenet
        
        """
        print('Verificando se a internet está funcionando')
        time.sleep(5)
        conectar = requisicao.conectar()

        print(conectar)
        while conectar[0] == 2:
            """  
            Verifica se está sem internet se estiver fica em um loop alimentado a variavel lista com todas as tentativas de 
            conexão
            
            """
            print('Sem internet', flush=True)
            time.sleep(1)
            sistema()

            conectar = requisicao.conectar()
            lista.append(conectar)

            if conectar[0] == 1:
                """
                Verifica se está conectado, só vai funcionar se antes estava sem internet. pega essa lista que foi
                alimentada e joga em um arquivo CSV para informar a hora que caiu e a hora que retornou.
                
                Faz um teste de velocidade
                 """
                print('Internet restabelecida', flush=True)
                time.sleep(1)
                sistema()

                conectar = requisicao.conectar()
                lista.append(conectar)
                diferenca = requisicao.diferenca(lista)
                # sem internet
                lista.clear()
                push = conexao.pushbullet(diferenca)
                velocidade = requisicao.speed()
                clima = conexao.getClima(cidade)
                salvar = requisicao.salvar(*diferenca, velocidade, clima, path=path)  # Salva essa diferença em um arquivo CSV
                break

        mensagem = 'Internet sem falha'
        tempo = requisicao.cronometro(1, mensagem)
        hoje = datetime.date.today()
        print(hoje)
