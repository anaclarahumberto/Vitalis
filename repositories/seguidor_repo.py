from typing import List
from sql.seguidor_sql import *
from util.database import obter_conexao
from models.seguidor_model import Seguidor  

class SeguidorRepo:
    @classmethod
    def criar_tabela(cls):
        """Cria a tabela de seguidores se não existir"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_SEGUIDORES)

    @classmethod
    def seguir_usuario(cls, id_usuario_seguidor: int, id_usuario_seguido: int) -> bool:
        """Insere uma nova relação de seguimento na tabela de seguidores"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_INSERIR_SEGUIDOR, (id_usuario_seguidor, id_usuario_seguido))
            return cursor.rowcount > 0  # Retorna True se a inserção foi bem-sucedida

    @classmethod
    def deixar_de_seguir(cls, id_usuario_seguidor: int, id_usuario_seguido: int) -> bool:
        """Remove a relação de seguimento entre dois usuários"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_DELETAR_SEGUIDOR, (id_usuario_seguidor, id_usuario_seguido))
            return cursor.rowcount > 0  # Retorna True se a remoção foi bem-sucedida

    @classmethod
    def obter_seguidores(cls, id_usuario: int) -> List[int]:
        """Retorna uma lista com os ids dos seguidores de um usuário"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_SEGUIDORES, (id_usuario,))
            seguidores = [row[0] for row in cursor.fetchall()]  # Retorna uma lista de ids de seguidores
            return seguidores

    @classmethod
    def obter_seguindo(cls, id_usuario: int) -> List[int]:
        """Retorna uma lista com os ids dos usuários que o usuário está seguindo"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_SEGUINDO, (id_usuario,))
            seguindo = [row[0] for row in cursor.fetchall()]  # Retorna uma lista de ids de usuários seguidos
            return seguindo

    @classmethod
    def obter_numero_seguidores(cls, id_usuario: int) -> int:
        """Retorna o número de seguidores de um usuário"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_NUMERO_SEGUIDORES, (id_usuario,))
            numero_seguidores = cursor.fetchone()[0]  # Pega o valor do COUNT(*)
            return numero_seguidores

    @classmethod
    def obter_numero_seguindo(cls, id_usuario: int) -> int:
        """Retorna o número de usuários que um usuário está seguindo"""
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_NUMERO_SEGUINDO, (id_usuario,))
            numero_seguindo = cursor.fetchone()[0]  # Pega o valor do COUNT(*)
            return numero_seguindo
        
    @classmethod
    def verificar_seguindo(cls, id_usuario_seguidor: int, id_usuario_seguido: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_VERIFICAR_SEGUINDO, (id_usuario_seguidor, id_usuario_seguido))
            return cursor.fetchone() is not None
