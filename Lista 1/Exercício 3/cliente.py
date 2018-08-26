""" Cliente """
import socket, pickle, notas

def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    grades = notas.Notas()
    grades.N1 = float(input(" Nota 1: "))  # recebe a nota 1
    grades.N2 = float(input(" Nota 2: "))  # recebe a nota 2
    grades.N3 = float(input(" Nota 3: "))  # recebe a nota 3

    socket_cliente.send(pickle.dumps(grades))

    socket_cliente.close()  # fecha a conexão

if __name__ == '__main__':
    programa_cliente()
