import sqlite3
from contextlib import contextmanager

from sql.cadastro_temp_sql import *
from util.database import obter_conexao


class CadastroTempRepo:
    @classmethod
    def criar_tabela_temp(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_TEMP)
            db.commit()
            cursor.execute(SQL_VERIFICAR_TRIGGER_EXPIRACAO)
            trigger_exists = cursor.fetchone()

            if not trigger_exists:
                cursor.execute(SQL_CRIAR_TRIGGER_EXPIRACAO)
                db.commit()

    @classmethod
    def inserir_dados(cls, id_usuario, nome=None, nome_perfil = None, email=None, senha_hash=None) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_INSERIR_TEMP, (id_usuario, nome, nome_perfil, email, senha_hash))
            db.commit()

    @classmethod
    def atualizar_data(cls, id_usuario, data_nascimento=None,) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_ATUALIZAR_DATA_TEMP, (data_nascimento, id_usuario))
            db.commit()

    @classmethod
    def obter_dados(cls, id_usuario):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_DADOS_TEMP, (id_usuario,))
            return cursor.fetchone()

    @classmethod
    def remover_dados(cls, id_usuario):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_REMOVER_DADOS_TEMP, (id_usuario,))
            db.commit()

    @classmethod
    def mover_para_banco_real(cls, id_usuario):
        dados = cls.obter_dados(id_usuario)
        if not dados:
            return None
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_INSERIR_USUARIO_REAL, dados)
            db.commit()
        cls.remover_dados(id_usuario)
        return dados
