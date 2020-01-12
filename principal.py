import datetime
import os
import time
import sys

import conexao
from conexao import Requisicao

url = 'https://www.google.com/'
path = 'log.csv'
requisicao = Requisicao(url)
lista = []
if __name__ == '__main__':

    """
    Menu simples
    
    """
    escolha = 0
    while True:
        print('***' * 10, 'MENU', '***' * 10)
        print('Por favor escolha uma alternativa: ')
        print('Digite 1 para relatorio de desconto')
        print('Digite 2 para começar uma analise da sua internet')
        print('***' * 20)
        escolha = int(input(': '))

        time.sleep(1)
        os.system('cls')
        if escolha == 1:
            os.system('cls')
            requisicao.relatorio()
            print('***' * 20)
            print(requisicao.desconto())
            time.sleep(5)
            print('***' * 10, 'MENU', '***' * 10)
            print('Pressione 1 relatorio de desconto novamente :')
            print('Pressione 2 para continuar com a verificação da sua internet:')
            print('Digite 3 para fechar o programa')
            print('***' * 20)
            escolha = int(input(': '))
            if escolha == 1:
                os.system('cls')
                requisicao.relatorio()
                print('***' * 20)
                print(requisicao.desconto())
                time.sleep(5)
            elif escolha == 2:
                break
            else:
                sys.exit()
        else:
            break




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
            os.system('cls')

            conectar = requisicao.conectar()
            lista.append(conectar)

            if conectar[0] == 1:
                """
                Verifica se está conectado, só vai funcionar se antes estava sem internet. pega essa lista que foi
                alimentada e joga em um arquivo CSV para informar a hora que caiu e a hora que retornou.
                
                Faz um teste de velocidade
                 """


                conectar = requisicao.conectar()
                lista.append(conectar)
                diferenca = requisicao.diferenca(lista,'Rio de Janeiro')
                # sem internet
                lista.clear()
                push = conexao.pushbullet(diferenca)
                salvar = requisicao.salvar(diferenca, path)  # Salva essa diferença em um arquivo CSV
                break

        mensagem = 'Internet sem falha'
        tempo = requisicao.cronometro(1, mensagem)
        hoje = datetime.date.today()
        print(hoje)
