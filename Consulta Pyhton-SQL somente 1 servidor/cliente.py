""" Cliente """
import socket

def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    while True:
        resposta = socket_cliente.recv(1024).decode() # recebe a resposta e a decodifica

        print(resposta)

        opcao_tabela = input()

        if int(opcao_tabela) < 0:
            break

        socket_cliente.send(opcao_tabela.encode()) # envia a mensagem codificada
        resposta = socket_cliente.recv(1024).decode() # recebe a resposta e a decodifica

        print(resposta)

        opcao_coluna = input()

        if int(opcao_coluna) < 0:
            break

        socket_cliente.send(opcao_coluna.encode()) # envia a mensagem codificada
        resposta = socket_cliente.recv(102400).decode() # recebe a resposta e a decodifica

        print(resposta)

        deseja_continuar = input("\nDeseja continuar consultando? S/N: ")

        if deseja_continuar is 'N':
            break

    socket_cliente.close()  # fecha a conexão


if __name__ == '__main__':
    programa_cliente()
