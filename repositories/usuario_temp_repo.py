from datetime import date
import sqlite3
from contextlib import contextmanager

from models.usuario_model import Usuario
from sql.cadastro_temp_sql import *
from util.database import obter_conexao


class UsuarioTempRepo:
    @classmethod
    def criar_tabela_temp(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_APAGAR_TABELA_TEMP)
            cursor.execute(SQL_CRIAR_TABELA_TEMP)
            db.commit()
            cursor.execute(SQL_VERIFICAR_TRIGGER_EXPIRACAO)
            trigger_exists = cursor.fetchone()

            if not trigger_exists:
                cursor.execute(SQL_CRIAR_TRIGGER_EXPIRACAO)
                db.commit()

    @classmethod
    def inserir_dados(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_INSERIR_TEMP, (usuario.nome, usuario.nome_perfil, usuario.email, usuario.senha))
            db.commit()

    @classmethod
    def atualizar_data(cls, data_nascimento: date, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_ATUALIZAR_DATA_TEMP, (data_nascimento, email))
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
