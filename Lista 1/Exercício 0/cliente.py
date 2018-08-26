""" Cliente do 'chat' """
import socket


def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    mensagem = input(" -> ")  # recebe a entrada

    while mensagem.lower().strip() != 'tchau':
        socket_cliente.send(mensagem.encode())  # envia a mensagem codificada
        dado = socket_cliente.recv(1024).decode()  # recebe a resposta e a decodifica

        print('Servidor: ' + dado)  # mostra a mensagem no terminal

        mensagem = input(" -> ")  # recebe outra entrada

    socket_cliente.close()  # fecha a conexão


if __name__ == '__main__':
    programa_cliente()
