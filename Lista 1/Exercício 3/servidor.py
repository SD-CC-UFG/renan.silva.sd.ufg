""" Servidor """
import socket, pickle, notas

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
        grades_temp = conexao.recv(4096)
        grades = pickle.loads(grades_temp)

        M = (grades.N1 + grades.N2)/2.0

        if not grades:
            # se o dado não for recebido, sai do loop
            break
        elif M >= 7.00:
            print("O aluno está aprovado.")
            break
        elif M > 3.00 and M < 7.00:
            if ((M + grades.N3)/2.00) >= 5.00:
                print("O aluno está aprovado.")
                break
        
        print("O aluno está reprovado.")
        break

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
