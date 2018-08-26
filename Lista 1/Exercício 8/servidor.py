""" Servidor """
import socket, pickle

def programa_servidor():
    """ Função para abrir o programa do servidor """

    # pega o nome do host
    host = socket.gethostname()
    porta = 5000  # utilizar uma porta acima de 1024

    socket_servidor = socket.socket()  # pega a instância do socket do servidor
    socket_servidor.bind((host, porta))  # liga o host com a porta, utiliza uma tupla como argumento

    # listen configura quantos clientes o servidor pode ouvir ao mesmo tempo
    socket_servidor.listen(2)
    conexao, endereco = socket_servidor.accept()  # aceita uma nova conexão
    print("Conexão efetuada com sucesso do endereço: " + str(endereco))

    while True:
        # recebe o fluxo de dados e o decodifica, não é aceito um pacote maior que 4 kB
        saldo_temp = conexao.recv(4096)
        saldo_medio = pickle.loads(saldo_temp)

        if saldo_medio < 0:
            # se o saldo_medio for menor ou igual a 0, sai do loop
            break
        elif saldo_medio >= 0 and saldo_medio <= 200:
            print("Saldo médio: " + repr(saldo_medio) + "\nPercentual de crédito: 0.00")
            break
        elif saldo_medio >= 201 and saldo_medio <= 400:
            print("Saldo médio: " + repr(saldo_medio) + "\nPercentual de crédito: " + repr(saldo_medio * 0.2))
            break
        elif saldo_medio >= 401 and saldo_medio <= 600:
            print("Saldo médio: " + repr(saldo_medio) + "\nPercentual de crédito: " + repr(saldo_medio * 0.3))
            break

        print("Saldo médio: " + repr(saldo_medio) + "\nPercentual de crédito: " + repr(saldo_medio * 0.4))
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
