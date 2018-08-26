""" Cliente """
import socket, pickle, pessoa

def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    pess = pessoa.Pessoa()
    pess.altura = float(input(" Altura: "))  # recebe a altura
    pess.sexo = input(" Sexo: ")  # recebe o sexo
    socket_cliente.send(pickle.dumps(pess))

    socket_cliente.close()  # fecha a conexão

if __name__ == '__main__':
    programa_cliente()
