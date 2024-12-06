from typing import List
from sql.curtida_sql import *
from util.database import obter_conexao
from models.curtida_model import Curtida 

class CurtidaRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_CURTIDA)

    @classmethod
    def curtir_publicacao(cls, id_publicacao: int, id_usuario: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_INSERIR_CURTIDA, (id_publicacao, id_usuario))
            return cursor.rowcount > 0  

    @classmethod
    def remover_curtida_publicacao(cls, id_publicacao: int, id_usuario: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_DELETAR_CURTIDA, (id_publicacao, id_usuario))
            return cursor.rowcount > 0  

    @classmethod
    def obter_curtidas(cls, id_publicacao: int) -> List[int]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_CURTIDAS, (id_publicacao,))
            seguidores = [row[0] for row in cursor.fetchall()]  
            return seguidores

    @classmethod
    def obter_numero_curtidas(cls, id_publicacao: int) -> int:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_NUMERO_CURTIDAS, (id_publicacao,))
            numero_seguidores = cursor.fetchone()[0]  # Pega o valor do COUNT(*)
            return numero_seguidores
        
    @classmethod
    def verificar_curtida(cls, id_publicacao: int, id_usuario: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_VERIFICAR_CURTIDA, (id_publicacao, id_usuario))
            return cursor.fetchone() is not None
