SQL_CRIAR_TABELA_CURTIDA = """
    CREATE TABLE IF NOT EXISTS curtida (
        id_publicacao INTEGER NOT NULL, 
        id_usuario INTEGER NOT NULL, 
        PRIMARY KEY (id_publicacao, id_usuario),
        FOREIGN KEY (id_publicacao) REFERENCES publicacao (id_publicacao) ON DELETE CASCADE,
        FOREIGN KEY (id_usuario) REFERENCES usuario (id) ON DELETE CASCADE
    )
"""

SQL_INSERIR_CURTIDA = """
    INSERT INTO curtida (id_publicacao, id_usuario)
    VALUES (?, ?)
"""

SQL_DELETAR_CURTIDA = """
    DELETE FROM curtida
    WHERE id_publicacao = ? AND id_usuario = ?
"""

SQL_OBTER_NUMERO_CURTIDAS = """
    SELECT COUNT(*) FROM curtida
    WHERE id_publicacao = ?
"""

SQL_OBTER_CURTIDAS = """
    SELECT id_usuario FROM curtida 
    WHERE id_publicacao = ?
"""

SQL_VERIFICAR_CURTIDA = """
    SELECT 1 FROM curtida WHERE id_publicacao = ? AND id_usuario = ?
"""


