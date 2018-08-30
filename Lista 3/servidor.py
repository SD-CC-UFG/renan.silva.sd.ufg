import socket
import sys
import traceback
import threading

conexoes = {}
TAMANHO_MAXIMO_CONEXOES = 2

def iniciar_servidor():
    host = socket.gethostname()
    porta = 8888

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # A constante SO_REUSEADDR diz ao kernel para reutilizar um soquete local no estado TIME_WAIT, sem esperar que seu tempo limite natural expire
    # a função setsockopt deve definir a opção especificada pelo terceiro argumento (option_name), no nível do protocolo especificado pelo segundo argumento (level), 
    # para o valor apontado pelo quarto argumento (option_value) para o soquete associado ao descritor de arquivo especificado pelo primeiro argumento (soquete).
    print("Soquete criado")

    try:
        soc.bind((host, porta))
    except:
        print("Bind falhou. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(2)       # O comprimento máximo da fila de conexões pendentes é de TAMANHO_MAXIMO_CONEXOES.
    print("Soquete esperando cliente.")

    threads = []
    for i in range(TAMANHO_MAXIMO_CONEXOES):
        thread = threading.Thread(target=cliente_thread, args=(porta, soc))
        threads.append(thread)

    for i in range(TAMANHO_MAXIMO_CONEXOES):
        if len(conexoes) > TAMANHO_MAXIMO_CONEXOES:
            break

        conexao, endereco = soc.accept()
        ip, porta = str(endereco[0]), str(endereco[1])
        print("Conectado com " + ip + ":" + porta)
        conexoes[conexao] = ip
        threads[i].start()

    soc.close()


def cliente_thread(porta, soc, tamanho_maximo_buffer = 5120): # mb tamanho máximo do buffer
    esta_ativo = True

    while esta_ativo:
        for conexao, ip in conexoes.copy().items():
            cliente_input = receber_input(conexao, ip, porta, tamanho_maximo_buffer)

            if "--QUIT--" in cliente_input:
                print("Cliente está pedindo para sair")
                conexao.close()
                conexoes.pop(conexao)
                print("Conexão com " + str(ip) + ":" + str(porta) + " fechada.")
            elif "--QUIT SERVER--" in cliente_input:
                soc.close()
                conexoes.clear()
            else:
                print("Resultado processado: {}".format(cliente_input))
                conexao.sendall("-".encode("utf8"))
        
        if not conexoes:
            esta_ativo = False

def receber_input(conexao, ip, porta, tamanho_maximo_buffer):
    cliente_input = conexao.recv(tamanho_maximo_buffer)
    tamanho_cliente_input = sys.getsizeof(cliente_input)

    if tamanho_cliente_input > tamanho_maximo_buffer:
        print("O tamanho do input é maior do que o esperado {}".format(tamanho_cliente_input))

    input_decodificado = cliente_input.decode("utf8").rstrip()  # decodificar e retirar o final da linha se houver espaço vazio
    resultado = processar_input(input_decodificado, ip, porta)

    return resultado


def processar_input(input_str, ip, porta):
    print("Processando a entrada recebida pelo cliente...")

    return "Mensagem recebida do cliente " + str(ip) + ":" + str(porta) + " -> " + str(input_str).upper()

if __name__ == "__main__":
    iniciar_servidor()