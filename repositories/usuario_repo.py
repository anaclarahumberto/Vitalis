from datetime import date
from typing import Optional
from dtos.usuario_autenticado import UsuarioAutenticado
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.database import obter_conexao


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
            resultado =  cursor.execute(SQL_INSERIR_USUARIO, (usuario.nome, usuario.nome_perfil, usuario.email, usuario.cpf, usuario.telefone, usuario.data_nascimento, usuario.senha, usuario.tipo_perfil, usuario.registro_profissional,))
            return resultado.rowcount > 0
    
    @classmethod
    def inserir_data(cls, email: str, data: date) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_DATA,
                (data,
                 email))
            return resultado.rowcount > 0
    
    @classmethod
    def inserir_categoria_perfil(cls, email: str, perfil: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_CATEGORIA_PERFIL,
                (perfil, email))
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
    def inserir_dados_perfil(cls, nome_perfil: str, foto_perfil: bool, id) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_PERFIL, (nome_perfil,  foto_perfil, id))
            return resultado.rowcount > 0
        
    @classmethod
    def obter_dados_perfil(cls, id: int):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_DADOS_PERFIL, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return UsuarioAutenticado(
                    id = resultado[0],
                    nome = resultado[1],
                    nome_perfil = resultado[2],
                    email = resultado[3],
                    telefone = resultado[4],
                    bio_perfil = resultado[5],
                    categoria_perfil = resultado[6],
                    genero = resultado[7],
                    foto_perfil= resultado[8],
                    tipo_perfil= resultado[9],
                )
            return None  
        
    @classmethod
    def obter_dados_perfil_seguido(cls, id: int):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_DADOS_PERFIL_SEGUIDO, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return UsuarioAutenticado(
                    id = resultado[0],
                    nome_perfil = resultado[1],
                    foto_perfil= resultado[2],
                    tipo_perfil= resultado[3],
                )
            return None

        
         
    @classmethod
    def atualizar_dados_perfil(cls, foto_perfil: bool, nome:  str, nome_perfil: str, telefone: str, bio_perfil: str, categoria: str, genero: str, id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_DADOS, (foto_perfil, nome, nome_perfil, telefone, bio_perfil, categoria, genero, id))
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
                        id = dados[0],
                        nome = dados[1],
                        nome_perfil = dados[2],
                        foto_perfil = dados[4],
                        tipo_perfil = dados[5],
                    )
            return None
        
    @classmethod
    def verificar_foto_perfil(cls, id: int):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_FOTO_PERFIL, (id,))
            resultado = cursor.fetchone()  
            
            if resultado is not None:
                return resultado[0]
            else:
                return False

    
    @classmethod
    def excluir_usuario(cls, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_USUARIO, (email,))
            return resultado.rowcount > 0
        
    @classmethod
    def is_email_unique(cls, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_EMAIL_UNICO, (email,))
            return cursor.fetchone() is None
        
    @classmethod
    def is_cpf_unique(cls, cpf: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_CPF_UNICO, (cpf,))
            return cursor.fetchone() is None
    
    @classmethod
    def is_phone_unique(cls, telefone: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_TELEFONE_UNICO, (telefone,))
            return cursor.fetchone() is None

    @classmethod
    def is_username_unique(cls, username: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CHECAR_NOME_PERFIL_UNICO, (username,))
            return cursor.fetchone() is None  

    @classmethod
    def pesquisar_perfil(cls, nome_perfil: str) -> list:
        with obter_conexao() as db:
            cursor = db.cursor()
            parametro = f"%{nome_perfil}%"
            cursor.execute(SQL_PESQUISAR_USUARIOS, (parametro,))
            registros = cursor.fetchall()
            usuarios_correspondentes  = []
            for registro in registros:
                foto_perfil = registro[3]  
                foto_url = f"/static/img/{registro[0]}.jpeg" if foto_perfil else "/static/img/usuario.jpg"
                usuario_correspondente = Usuario(
                    id= registro[0],
                    nome= registro[1],
                    nome_perfil= registro[2],
                    foto_url= foto_url
                )
                usuarios_correspondentes.append(usuario_correspondente)
            return usuarios_correspondentes   