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
        idade_temp = conexao.recv(4096)
        idade = pickle.loads(idade_temp)

        if idade <= 0:
            # se idade for menor ou igual a 0, sai do loop
            break
        elif idade >= 5 and idade <= 7:
            print("Categoria Infantil A.")
            break
        elif idade >= 8 and idade <= 10:
            print("Categoria Infantil B.")
            break
        elif idade >= 11 and idade <= 13:
            print("Categoria Juvenil A.")
            break
        elif idade >= 14 and idade <= 17:
            print("Categoria Juvenil B.")
            break
        elif idade >= 18:
            print("Categoria Adulto.")
            break
        
        print("Muito novo para nadar.")
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
