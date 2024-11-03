# Importando bibliotecas Sqlite3 e DateTime
import sqlite3
from datetime import datetime

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criando tabela produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_produtos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               categoria TEXT,
               quantidade INTEGER NOT NULL,
               preco REAL NOT NULL,
               localizacao TEXT NOT NULL,
               data_entrada TEXT
)
''')
conn.commit()

# Método para formatar a exibição de um produto
def formatar_produto(produto):
    return (f"\nProduto: {produto[1]} - Categoria: {produto[2]} - "
            f"Quantidade: {produto[3]} - Preço R$: {produto[4]:.2f} - "
            f"Localização no depósito: {produto[5]} - "
            f"Data de Entrada: {produto[6]}\n")

# Método para cadastrar um produto
def cadastrar_produto(nome, categoria, quantidade, preco, localizacao):
    data_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO tb_produtos (nome, categoria, quantidade, preco, localizacao, data_entrada) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade, preco, localizacao, data_entrada))
    conn.commit()
    print(f"Produto: '{nome}' cadastrado com sucesso!")

# Método para atualizar quantidade em estoque
def atualizar_estoque(id_produto, quantidade, adicionar = True):
    cursor.execute('SELECT quantidade FROM tb_produtos WHERE id = ?', (id_produto,))
    produto = cursor.fetchone()
    
    if produto:
        nova_quantidade = produto[0] + quantidade if adicionar else produto[0] - quantidade
        if nova_quantidade < 0:
            print(f"\nNão é possível remover {quantidade}. Estoque atual: {produto[0]}.")
        else:
            cursor.execute('''
            UPDATE tb_produtos SET quantidade = ? WHERE id = ?
            ''', (nova_quantidade, id_produto))
            conn.commit()
            operacao = "adicionado" if adicionar else "removido"
            print(f"\n{quantidade} unidades {operacao} com sucesso para o produto ID: {id_produto}. Novo estoque do produto: {nova_quantidade}.")
    else:
        print("Produto não encontrado.")

# Método para rastrear localização do produto
def rastrear_localizacao(id_produto):
    cursor.execute('''
    SELECT localizacao FROM tb_produtos WHERE id = ?
    ''', (id_produto,))
    localizacao = cursor.fetchone()
    if localizacao:
        print(f"\nLocalização do produto ID: {id_produto}: {localizacao[0]}")
    else:
        print("Produto não encontrado.")

# Método para gerar relatórios
def gerar_relatorio():
    print("\nRelatório de estoque")
    print("--------------------")

    # Produtos com estoque baixo (menos de 5 unidades)
    cursor.execute('''
    SELECT * FROM tb_produtos WHERE quantidade < 5
    ''')
    baixo_estoque = cursor.fetchall()
    if baixo_estoque:
        print("\nATENÇÃO: Produto com estoque baixo!\n")
        for produto in baixo_estoque:
            print(formatar_produto(produto))
    else:
        print("\nNão há produtos com estoque baixo!")

    # Produtos com excesso de estoque (mais de 50 unidades)
    cursor.execute('''
    SELECT * FROM tb_produtos WHERE quantidade > 50
    ''')
    excesso_estoque = cursor.fetchall()
    if excesso_estoque:
        print("\nATENÇÃO: Produtos com excesso de estoque:\n")
        for produto in excesso_estoque:
            print(formatar_produto(produto))
    else:
        print("\nNão há produtos com excesso de estoque.")

    # Movimentação de produtos (últimos 5 produtos cadastrados)
    cursor.execute('''
    SELECT * FROM tb_produtos ORDER BY data_entrada DESC LIMIT 5
    ''')
    movimentacao = cursor.fetchall()
    if movimentacao:
        print("\nÚltimos produtos cadastrados:")
        for produto in movimentacao:
            print(formatar_produto(produto))
    else:
        print("\nNão há movimentação de produtos.")

# Método para listar todos os produtos no estoque
def listar_produtos():
    cursor.execute('SELECT * FROM tb_produtos')
    produtos = cursor.fetchall()
    print("\nLista de produtos em estoque")
    print("----------------------------")
    for produto in produtos:
        print(formatar_produto(produto))

# Menu principal do sistema
def menu():
    while True:
        print("\n=========================================================")
        print("GSV STOCK SOLUTIONS - SISTEMA DE GERENCIAMENTO DE ESTOQUE")
        print("=========================================================\n")
        print("[1] - Cadastrar novo produto")
        print("[2] - Atualizar quantidade em estoque")
        print("[3] - Rastrear localização do produto")
        print("[4] - Gerar relatório de estoque")
        print("[5] - Listar todos os produtos no estoque")
        print("[6] - Sair\n")

        opcao = int(input("\nEscolha uma opção: "))

        if opcao == 1:
            print("\nCADASTRO DE PRODUTO")
            print("===================\n")
            nome = input("Nome do produto: ")
            categoria = input("Categoria: ")
            quantidade = int(input("Quantidade em estoque: "))
            preco = float(input("Preço do produto R$: "))
            localizacao = input("Localização no depósito: ")
            cadastrar_produto(nome, categoria, quantidade, preco, localizacao)

        elif opcao == 2:
            id_produto = int(input("\nDigite o código do produto que deseja atualizar: "))
            operacao = input("Digite [A] para adicionar ou [R] para remover: ").strip().upper()
            quantidade = int(input("Quantidade: "))

            if operacao == 'A':
                atualizar_estoque(id_produto, quantidade, adicionar=True)
            elif operacao == 'R':
                atualizar_estoque(id_produto, quantidade, adicionar=False)
            else:
                print("Opção inválida! Escolha 'A' para adicionar ou 'R' para remover.")

        elif opcao == 3:
            id_produto = int(input("\nDigite o código do produto para rastrear a localização: "))
            rastrear_localizacao(id_produto)

        elif opcao == 4:
            gerar_relatorio()

        elif opcao == 5:
            listar_produtos()

        elif opcao == 6:
            print("\nOBRIGADO POR UTILIZAR NOSSOS SERVIÇOS, PROGRAMA ENCERRADO!")
            break

        else:
            print("ATENÇÃO: Opção inválida!")

# Executa o sistema
menu()

# Fecha conexão com banco de dados
conn.close()








