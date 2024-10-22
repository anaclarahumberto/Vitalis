SQL_APAGAR_TABELA = """
    DROP TABLE IF EXISTS usuario
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    data_nascimento DATE NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    telefone TEXT UNIQUE,
    cpf TEXT UNIQUE,
    endereco_cep TEXT,
    endereco_logradouro TEXT,
    endereco_numero TEXT,
    endereco_complemento TEXT,
    endereco_bairro TEXT,
    endereco_cidade TEXT,
    endereco_uf   TEXT,
    foto_perfil BOOL,
    nome_perfil TEXT NOT NULL,
    bio_perfil TEXT,
    categoria_perfil TEXT,
    genero TEXT,
    tipo_perfil INTEGER,
    registro_profissional BOOL,
    tipo_paciente INTEGER )   
"""

# SQL_ATUALIZAR_TABELA = [
#     "ALTER TABLE usuario ADD COLUMN foto_perfil BOOL;",
#     "ALTER TABLE usuario ADD COLUMN nome_perfil TEXT;",
#     "ALTER TABLE usuario ADD COLUMN bio_perfil TEXT;",
#     "ALTER TABLE usuario ADD COLUMN categoria_perfil TEXT;",
#     "ALTER TABLE usuario ADD COLUMN genero TEXT;",
#     "ALTER TABLE usuario ADD COLUMN tipo_paciente TEXT;" 
# ]

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario 
    (nome, email, senha, nome_perfil)
    VALUES (?, ?, ?, ?)
"""

SQL_ATUALIZAR_DATA = """
    UPDATE usuario
    SET data_nascimento = ?,
    WHERE EMAIL = ?
"""

SQL_OBTER_DADOS_PERFIL = """
    SELECT id, nome, nome_perfil, email, telefone, bio_perfil, categoria_perfil, genero
    FROM usuario
    WHERE email = ?
"""

SQL_ATUALIZAR_PERFIL = """
    UPDATE usuario
    SET nome_perfil = ?, foto_perfil = ?
    WHERE ID = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET nome = ?, nome_perfil = ?, telefone = ?, bio_perfil = ?, categoria_perfil = ?, genero = ?
    WHERE id = ?
"""

SQL_ATUALIZAR_ENDERECO = """
    UPDATE usuario SET
    endereco_cep = ?,
    endereco_logradouro = ?,
    endereco_numero = ?,
    endereco_complemento = ?,
    endereco_bairro = ?,
    endereco_cidade = ?,
    endereco_uf = ?)
    WHERE id = ?
"""

SQL_CHECAR_CREDENCIAIS = """
    SELECT id, nome, nome_perfil, email, senha
    FROM usuario
    WHERE email = ?
"""

SQL_CHECAR_ID = """
    SELECT id FROM usuario WHERE email = ?
"""

SQL_CHECAR_FOTO_PERFIL = """
    SELECT foto_perfil FROM usuario WHERE id = ?
"""
SQL_CHECAR_EMAIL_UNICO = """SELECT 1 FROM usuario WHERE email = ?"""

SQL_CHECAR_NOME_PERFIL_UNICO = """SELECT 1 FROM usuario WHERE nome_perfil = ?"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""