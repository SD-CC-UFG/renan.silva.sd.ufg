import socket
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    porta = 8888

    try:
        soc.connect((host, porta))
    except:
        print("Erro de conexão.")
        sys.exit()

    print("Digite 'quit' para sair")
    message = input(" -> ")

    while message != 'quit' and message != 'quit server':
        soc.sendall(message.encode("utf8"))
        if soc.recv(5120).decode("utf8") == "-":
            pass

        message = input(" -> ")

    if message == 'quit server':
        soc.send(b'--quit server--')
    
    soc.send(b'--quit--')

if __name__ == "__main__":
    main()