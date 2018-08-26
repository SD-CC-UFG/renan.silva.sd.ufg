""" Cliente """
import socket, pickle

def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    saldo_medio = float(input(" Saldo médio do cliente: "))  # recebe o saldo médio do último ano de um cliente
    socket_cliente.send(pickle.dumps(saldo_medio))

    socket_cliente.close()  # fecha a conexão

if __name__ == '__main__':
    programa_cliente()
