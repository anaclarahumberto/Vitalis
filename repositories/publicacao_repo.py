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
        
    @classmethod
    def obter_numero_publicacoes(cls, id_usuario: int) -> int:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_NUMERO_PUBLICACOES, (id_usuario,))
            numero_publicacoes = cursor.fetchone()[0]  
            return numero_publicacoes
        
    @classmethod
    def obter_publicacoes_por_usuario(cls, id_usuario: int) -> list:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_PUBLICACOES_POR_USUARIO, (id_usuario,))
            registros = cursor.fetchall()
            publicacoes = []
            for registro in registros:
                publicacao = {
                    "id_publicacao": registro[0],
                    "data_criacao": registro[1],
                    "imagem": registro[2],
                    "id_usuario": registro[3],
                    "descricao": registro[4],
                    "curtidas": registro[5],
                    "comentarios": registro[6],
                }
                publicacoes.append(publicacao)
            return publicacoes 