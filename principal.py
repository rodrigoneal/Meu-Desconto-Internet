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
    while True:
        selecionar = requisicao.menu()
        if selecionar == 1:
            os.system('cls')
            relatorio_dia = requisicao.relatorio()
            time.sleep(5)
            os.system('cls')
        elif selecionar == 2:
            os.system('cls')
            relatorio_desconto = requisicao.mes()
            time.sleep(5)
            os.system('cls')
        elif selecionar == 3:
            os.system('cls')
            relatorio_desconto = requisicao.desconto()
            time.sleep(5)
            os.system('cls')
        elif selecionar == 4:
            os.system('cls')
            break
        elif selecionar == 5:
            sys.exit()
        else:
            os.system('cls')
            print('Favor digitar uma opção valida')
            os.system('cls')
            time.sleep(5)
            continue




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
