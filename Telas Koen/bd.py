import sqlite3
from datetime import datetime

# Conexão com o banco de dados em memória
conexao = sqlite3.connect(":memory:")
cursor = conexao.cursor()

# Criação das tabelas
cursor.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    data_nascimento DATE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    duracao INTEGER,
    imagem_url TEXT,
    trailer_url TEXT
);
""")

cursor.execute("""
CREATE TABLE sessao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filme_id INTEGER NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    FOREIGN KEY (filme_id) REFERENCES filmes(id)
);
""")

cursor.execute("""
CREATE TABLE assentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER NOT NULL,
    assento_codigo TEXT NOT NULL,
    disponivel BOOLEAN DEFAULT 1,
    FOREIGN KEY (sessao_id) REFERENCES sessao(id)
);
""")

cursor.execute("""
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    sessao_id INTEGER NOT NULL,
    total_pago REAL NOT NULL,
    data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (sessao_id) REFERENCES sessao(id)
);
""")

cursor.execute("""
CREATE TABLE venda_assentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    assento_id INTEGER NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (assento_id) REFERENCES assentos(id)
);
""")

cursor.execute("""
CREATE TABLE relatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    total_vendas REAL NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

print("Banco de dados em memória criado com sucesso!")

# Função para registrar uma compra
def registrar_compra(usuario_id, sessao_id, assentos, total_pago):
    # Insere a venda
    cursor.execute("""
    INSERT INTO vendas (usuario_id, sessao_id, total_pago)
    VALUES (?, ?, ?)
    """, (usuario_id, sessao_id, total_pago))
    venda_id = cursor.lastrowid

    # Atualiza os assentos vendidos
    for assento_id in assentos:
        cursor.execute("""
        INSERT INTO venda_assentos (venda_id, assento_id)
        VALUES (?, ?)
        """, (venda_id, assento_id))
        cursor.execute("UPDATE assentos SET disponivel = 0 WHERE id = ?", (assento_id,))

    # Atualiza o relatório
    cursor.execute("""
    INSERT INTO relatorios (data_inicio, data_fim, total_vendas)
    VALUES (?, ?, ?)
    """, (datetime.now().date(), datetime.now().date(), total_pago))

    print(f"Compra registrada: Venda {venda_id} para usuário {usuario_id}")

# Função para gerar relatório
def gerar_relatorio():
    cursor.execute("""
    SELECT * FROM relatorios
    """)
    relatorios = cursor.fetchall()
    print("Relatórios:")
    for rel in relatorios:
        print(rel)

# Exemplo de uso
# Criando dados fictícios
cursor.execute("INSERT INTO usuarios (nome, email, senha, data_nascimento) VALUES ('João Silva', 'joao@gmail.com', 'senha123', '2000-01-01')")
cursor.execute("INSERT INTO filmes (titulo, descricao, duracao) VALUES ('Se7en', 'Crime e mistério', 127)")
cursor.execute("INSERT INTO sessao (filme_id, data, horario) VALUES (1, '2024-12-05', '18:00')")
cursor.execute("INSERT INTO assentos (sessao_id, assento_codigo) VALUES (1, 'A1')")
cursor.execute("INSERT INTO assentos (sessao_id, assento_codigo) VALUES (1, 'A2')")

# Registrando uma compra
registrar_compra(1, 1, [1, 2], 40.00)

# Gerando relatório
gerar_relatorio()

# Fechando conexão
conexao.close()
