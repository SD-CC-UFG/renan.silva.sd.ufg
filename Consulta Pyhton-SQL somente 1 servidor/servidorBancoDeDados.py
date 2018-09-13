import pyodbc, pickle, socket

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'sistemasdistribuidosufg.database.windows.net' 
database = 'sistemasDistribuidos' 
username = 'rfsiilva' 
password = 'admin!123' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def consulta_tabelas():
    #Select nome de todas as tabelas
    cursor.execute("SELECT Name FROM sys.Tables") 

    row = cursor.fetchone()
    tabelas = []

    while row: 
        tabelas.append(str(row[0]))
        row = cursor.fetchone()
    
    return tabelas

def consulta_colunas(tabelas, opcao_tabela):
    #Select nome de todas as colunas da tabela
    cursor.execute("SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('SalesLT." + tabelas[opcao_tabela] + "')")

    row = cursor.fetchone()
    colunas = []

    while row: 
        colunas.append(str(row[1]))
        row = cursor.fetchone()
    
    return colunas

def select(colunas, opcao_coluna, tabelas, opcao_tabela):
    if opcao_coluna < 0:
        cursor.execute("SELECT * FROM SalesLT." + tabelas[opcao_tabela])
    else:
        cursor.execute("SELECT " + colunas[opcao_coluna] + " FROM SalesLT." + tabelas[opcao_tabela])
    
    row = cursor.fetchone()
    resultado = []

    while row: 
        resultado.append(str(row))
        row = cursor.fetchone()
    
    return resultado

def programa_servidor():
    """ Função para abrir o programa do servidor """

    # pega o nome do host
    host = socket.gethostname()
    porta = 5000  # utilizar uma porta acima de 1024

    socket_servidor = socket.socket()  # pega a instância do socket do servidor
    socket_servidor.bind((host, porta))  # liga o host com a porta, utiliza uma tupla como argumento

    socket_servidor.listen()
    conexao, endereco = socket_servidor.accept()  # aceita uma nova conexão
    print("Conexão efetuada com sucesso do endereço: " + str(endereco))

    while True:
        ############# Consulta de tabelas #############
        tabelas = consulta_tabelas()

        opcoes_tabelas = "\nDigite o numero correspondente a tabela que quer consultar: \n"
        for i in range(len(tabelas)):
            opcoes_tabelas += (str(i+1) + " - " + tabelas[i] + "\n")

        conexao.send(opcoes_tabelas.encode())

        opcao_tabela = conexao.recv(1024).decode()
        opcao_tabela = int(opcao_tabela) - 1

        if opcao_tabela < 0:
            break

        ############# Consulta de colunas #############
        colunas = consulta_colunas(tabelas, opcao_tabela)

        opcoes_colunas = "\nDigite o numero correspondente a coluna que quer utilizar: \n0 - *\n"
        for i in range(len(colunas)):
            opcoes_colunas += (str(i+1) + " - " + colunas[i] + "\n")

        conexao.send(opcoes_colunas.encode())

        opcao_coluna = int(conexao.recv(1024).decode()) - 1

        ############# Consulta Final #############
        resultado = select(colunas, opcao_coluna, tabelas, opcao_tabela)

        conexao.send(str(resultado).encode())  # envia o dado codificado para o cliente

    conexao.close()  # fecha a conexão

if __name__ == '__main__':
    programa_servidor()
    #consulta_banco()