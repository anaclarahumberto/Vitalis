SQL_APAGAR_TABELA_TEMP = '''
    DROP TABLE IF EXISTS usuario_temp 
'''

SQL_CRIAR_TABELA_TEMP = '''
    CREATE TABLE IF NOT EXISTS usuario_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        nome_perfil TEXT,
        email TEXT,
        senha TEXT,
        data_nascimento DATE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
'''

SQL_VERIFICAR_TRIGGER_EXPIRACAO = """
    SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'limpar_registros_expirados';
"""

SQL_CRIAR_TRIGGER_EXPIRACAO = """
    CREATE TRIGGER limpar_registros_expirados
    AFTER INSERT ON usuario_temp
    BEGIN
        DELETE FROM usuario_temp
        WHERE created_at < datetime('now', '-10 minutes');
    END;
"""

SQL_INSERIR_TEMP = '''
    INSERT INTO usuario_temp (nome, nome_perfil, email, senha)
    VALUES (?, ?, ?, ?)
'''

SQL_ATUALIZAR_DATA_TEMP = '''
    UPDATE usuario_temp
    SET data_nascimento = ?
    WHERE email = ?
'''

SQL_OBTER_DADOS_TEMP = '''
    SELECT nome, nome_perfil, email, senha
        FROM usuario_temp 
        WHERE email = ?
'''

SQL_INSERIR_USUARIO_REAL = """
    INSERT INTO usuario 
    (nome, nome_perfil, email, senha, data_nascimento)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_REMOVER_DADOS_TEMP = '''
    DELETE FROM usuario_temp WHERE id_usuario = ?
'''