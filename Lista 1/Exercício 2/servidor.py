""" Servidor """
import socket, pickle, pessoa

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
        pess_temp = conexao.recv(4096)
        pess = pickle.loads(pess_temp)

        if not pess:
            # se o dado não for recebido, sai do loop
            break
        elif (pess.sexo.lower().strip() == 'feminino' and pess.idade >= 21) or (pess.sexo.lower().strip() == 'masculino' and pess.idade >= 18):
            print("A pessoa de nome '" + pess.nome + "' já atingiu a maioridade.")
            break
        elif pess.sexo.lower().strip() != 'masculino' and pess.sexo.lower().strip() != 'feminino':
            print('Sexo inválido.')
            break

        print("A pessoa de nome '" + pess.nome + "' ainda não atingiu a maioridade.")
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
