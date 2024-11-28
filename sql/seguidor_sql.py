SQL_CRIAR_TABELA_SEGUIDORES = """
    CREATE TABLE IF NOT EXISTS seguidores (
        id_usuario_seguidor INTEGER NOT NULL, 
        id_usuario_seguido INTEGER NOT NULL, 
        PRIMARY KEY (id_usuario_seguidor, id_usuario_seguido),
        FOREIGN KEY (id_usuario_seguidor) REFERENCES usuario (id) ON DELETE CASCADE,
        FOREIGN KEY (id_usuario_seguido) REFERENCES usuario (id) ON DELETE CASCADE
    )
"""

SQL_INSERIR_SEGUIDOR = """
    INSERT INTO seguidores (id_usuario_seguidor, id_usuario_seguido)
    VALUES (?, ?)
"""

SQL_DELETAR_SEGUIDOR = """
    DELETE FROM seguidores 
    WHERE id_usuario_seguidor = ? AND id_usuario_seguido = ?
"""

SQL_OBTER_NUMERO_SEGUIDORES = """
    SELECT COUNT(*) FROM seguidores 
    WHERE id_usuario_seguido = ?
"""

SQL_OBTER_SEGUIDORES = """
    SELECT id_usuario_seguidor FROM seguidores 
    WHERE id_usuario_seguido = ?
"""

SQL_OBTER_NUMERO_SEGUINDO = """
    SELECT COUNT(*) FROM seguidores 
    WHERE id_usuario_seguidor = ?
"""

SQL_OBTER_SEGUINDO = """
    SELECT id_usuario_seguido FROM seguidores 
    WHERE id_usuario_seguidor = ?
"""

SQL_VERIFICAR_SEGUINDO = """
    SELECT 1 FROM seguidores WHERE id_usuario_seguidor = ? AND id_usuario_seguido = ?
"""


