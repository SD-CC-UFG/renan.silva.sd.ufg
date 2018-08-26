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
        elif func.nivel.upper().strip() == 'A':
            if func.numero_dependentes == 0:
                salario_liquido = func.salario_bruto * 0.97
                break
            salario_liquido = func.salario_bruto * 0.92
            break
        elif func.nivel.upper().strip() == 'B':
            if func.numero_dependentes == 0:
                salario_liquido = func.salario_bruto * 0.95
                break
            salario_liquido = func.salario_bruto * 0.9
            break
        elif func.nivel.upper().strip() == 'C':
            if func.numero_dependentes == 0:
                salario_liquido = func.salario_bruto * 0.92
                break
            salario_liquido = func.salario_bruto * 0.85
            break
        elif func.nivel.upper().strip() == 'D':
            if func.numero_dependentes == 0:
                salario_liquido = func.salario_bruto * 0.9
                break
            salario_liquido = func.salario_bruto * 0.83
            break

        break

    print('O funcionário ' + func.nome + ' do nível ' + func.nivel.upper().strip() + ' recebe de salário líquido ' + repr(salario_liquido) + ' reais.')

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
