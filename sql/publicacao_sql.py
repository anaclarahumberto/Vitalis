SQL_APAGAR_TABELA_PUBLICACAO = """
    DROP TABLE IF EXISTS publicacao
"""

SQL_CRIAR_TABELA_PUBLICACAO = """
    CREATE TABLE IF NOT EXISTS publicacao (
    id_publicacao INTEGER PRIMARY KEY AUTOINCREMENT, 
    data_criacao DATE NOT NULL, 
    imagem TEXT NOT NULL,
    id_usuario TEXT NOT NULL,
    descricao TEXT,
    curtidas INTEGER,
    comentarios INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuario (id) ON DELETE CASCADE )
"""

SQL_INSERIR_PUBLICACAO = """
    INSERT INTO publicacao 
    (descricao, imagem, id_usuario, data_criacao)
    VALUES (?, ?, ?, ?)
"""

SQL_OBTER_NUMERO_PUBLICACOES = """
    SELECT COUNT(*) FROM publicacao 
    WHERE id_usuario = ?
"""

SQL_OBTER_PUBLICACOES_POR_USUARIO = """
    SELECT * FROM publicacao WHERE id_usuario = ?
"""

