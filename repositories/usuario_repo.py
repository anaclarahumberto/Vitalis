from datetime import date
from typing import Optional
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.db import obter_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

        
    @classmethod
    def inserir(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_USUARIO,
                (usuario.nome,
                 usuario.data_nascimento,
                 usuario.email,
                 usuario.cpf,
                 usuario.telefone,
                 usuario.senha,
                 usuario.perfil,
                 usuario.registro_profissional))
            return resultado.rowcount > 0
    
    @classmethod
    def inserir_perfil(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_PERFIL,
                (usuario.nome_perfil,
                 usuario.descricao_perfil,
                 usuario.categoria_perfil,
                 usuario.genero,
                 usuario.id))
            return resultado.rowcount > 0
        
    @classmethod
    def inserir_endereco(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_ENDERECO,
                (usuario.endereco_cep,
                 usuario.endereco_logradouro,
                 usuario.endereco_numero,
                 usuario.endereco_complemento,
                 usuario.endereco_bairro,
                 usuario.endereco_cidade,
                 usuario.endereco_uf,
                 usuario.id))
            return resultado.rowcount > 0
        
    @classmethod
    def obter_dados_perfil(cls, email: str):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_DADOS_PERFIL, (email,))
            resultado = cursor.fetchone()
            if resultado:
                return Usuario(
                    id = resultado[0],
                    nome = resultado[1],
                    nome_perfil = resultado[2],
                    email = resultado[3],
                    telefone = resultado[4],
                    bio_perfil = resultado[5],
                    categoria_perfil = resultado[6],
                    genero = resultado[7],
                )
            return None  

        
    @classmethod
    def obter_id_por_email(cls, email: str) -> Optional[int]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_ID, (email,))
            dados = cursor.fetchone()
            return dados[0] if dados else None
         
    @classmethod
    def atualizar_dados_perfil(cls, nome:  str, nome_perfil: str, email: str, telefone: str, bio_perfil: str, categoria: str, genero: str, email_atual: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_DADOS, (nome, nome_perfil, email, telefone, bio_perfil, categoria, genero, email_atual))
            return resultado.rowcount > 0
    
    @classmethod
    def atualizar_senha(cls, email: str, senha: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_SENHA, (senha, email))
            return resultado.rowcount > 0
      
    @classmethod
    def checar_credenciais(cls, email: str, senha: str) -> Optional[tuple]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_CHECAR_CREDENCIAIS, (email,)).fetchone()
            if dados:
                if conferir_senha(senha, dados[3]):
                    return Usuario(
                        nome = dados[0],
                        email = dados[1],
                        perfil = dados[2]
                    )
            return None
    
    @classmethod
    def excluir_usuario(cls, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_USUARIO, (email,))
            return resultado.rowcount > 0    