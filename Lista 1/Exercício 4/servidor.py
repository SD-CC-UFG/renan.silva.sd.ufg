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
        elif pess.sexo.lower().strip() == "masculino":
            peso_ideal = (72.7 * pess.altura) - 58

            print(repr(peso_ideal))
            break
        elif pess.sexo.lower().strip() == "feminino":
            peso_ideal = (62.1 * pess.altura) - 44.7
            
            print(repr(peso_ideal))
            break
        
        print("Sexo inválido.")
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
