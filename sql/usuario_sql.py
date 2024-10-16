SQL_APAGAR_TABELA = """
    DROP TABLE IF EXISTS usuario
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone TEXT NOT NULL UNIQUE, 
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    perfil INTEGER NOT NULL,
    endereco_cep TEXT,
    endereco_logradouro TEXT,
    endereco_numero TEXT,
    endereco_complemento TEXT,
    endereco_bairro TEXT,
    endereco_cidade TEXT,
    endereco_uf   TEXT,
    registro_profissional BOOL)
    
"""

SQL_ATUALIZAR_TABELA = [
    "ALTER TABLE usuario ADD COLUMN foto_perfil BOOL;",
    "ALTER TABLE usuario ADD COLUMN nome_perfil TEXT;",
    "ALTER TABLE usuario ADD COLUMN bio_perfil TEXT;",
    "ALTER TABLE usuario ADD COLUMN categoria_perfil TEXT;",
    "ALTER TABLE usuario ADD COLUMN genero TEXT;",
    "ALTER TABLE usuario ADD COLUMN tipo_paciente TEXT;" 
]

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario 
    (nome, data_nascimento, email, cpf, telefone, senha, perfil, registro_profissional)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
    SET nome = ?, nome_perfil = ?, email = ?, telefone = ?, bio_perfil = ?, categoria_perfil = ?, genero = ?
    WHERE email = ?
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
    SELECT id, nome, nome_perfil, email, perfil, senha
    FROM usuario
    WHERE email = ?
"""

SQL_CHECAR_ID = """
    SELECT id FROM usuario WHERE email = ?
"""

SQL_CHECAR_FOTO_PERFIL = """
    SELECT foto_perfil FROM usuario WHERE id = ?
"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""