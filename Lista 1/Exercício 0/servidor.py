""" Servidor do 'chat' """

import socket

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
        # recebe o fluxo de dados e o decodifica, não é aceito um pacote maior que 1 kB
        dado = conexao.recv(1024).decode()

        if not dado:
            # se o dado não for recebido, sai do loop
            break
        print("Cliente: " + str(dado))
        dado = input(' -> ')
        conexao.send(dado.encode())  # envia o dado codificado para o cliente

    conexao.close()  # fecha a conexão


if __name__ == '__main__':
    programa_servidor()
