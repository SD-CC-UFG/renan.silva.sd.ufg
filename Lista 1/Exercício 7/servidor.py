""" Servidor """
import socket, pickle, funcionario

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
        func_temp = conexao.recv(4096)
        func = pickle.loads(func_temp)

        if not func:
            # se o dado não for recebido, sai do loop
            break
        elif func.idade >= 65 and func.tempo_servico >= 30 and (func.idade >= 60 and func.tempo_servico >= 25):
            print("O funcionário já pode se aposentar.")
            break

        print('O funcionário ainda não pode se aposentar.')
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
