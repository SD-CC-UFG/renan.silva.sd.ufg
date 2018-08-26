""" Cliente """
import socket, pickle, funcionario

def programa_cliente():
    """ Função para abrir o programa do cliente """

    # como os dois códigos estão rodando na mesma máquina, o host é o mesmo
    host = socket.gethostname()
    porta = 5000  # o número da porta do socket do servidor

    socket_cliente = socket.socket()  # pega a instância do socket do cliente
    socket_cliente.connect((host, porta))  # estabelece a conexão com o servidor através da tupla

    func = funcionario.Funcionario()
    func.nome = input(" Nome: ")  # recebe o nome
    func.nivel = input(" Nível: ")  # recebe o nível
    func.salario_bruto = float(input(" Salário bruto: "))  # recebe o salário bruto
    func.numero_dependentes = int(input(" Número de dependentes: "))  # recebe o número de dependentes

    socket_cliente.send(pickle.dumps(func))

    socket_cliente.close()  # fecha a conexão


if __name__ == '__main__':
    programa_cliente()
