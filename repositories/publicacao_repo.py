from datetime import date
from typing import Optional
from models.comentarios_model import Publicacao
from sql.publicacao_sql import *
from util.database import obter_conexao


class PublicacaoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_PUBLICACAO)

    @classmethod
    def inserir(cls, publicacao: Publicacao) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado =  cursor.execute(SQL_INSERIR_PUBLICACAO, (publicacao.descricao, publicacao.imagem, publicacao.id_usuario, publicacao.data_criacao,))
            return resultado.rowcount > 0    