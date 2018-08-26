""" Servidor """
import socket, pickle, carta

def switch_valor(valor_card):
    switcher = {
        1: "ás",
        2: "dois",
        3: "três",
        4: "quatro",
        5: "cinco",
        6: "seis",
        7: "sete",
        8: "oito",
        9: "nove",
        10: "dez",
        11: "valete",
        12: "dama",
        13: "rei"
    }
    print(switcher.get(valor_card, "Valor de carta inválido."))

def switch_naipe(naipe_card):
    switchers = {
        1: "ouros",
        2: "paus",
        3: "copas",
        4: "espadas"
    }
    print(switchers.get(naipe_card, "Naipe de carta inválido."))

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
        card_temp = conexao.recv(4096)
        card = pickle.loads(card_temp)

        if not card:
            # se o dado não for recebido, sai do loop
            break

        print("A carta é " + switch_valor(card.valor) + " de " + switch_naipe(card.naipe))
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
