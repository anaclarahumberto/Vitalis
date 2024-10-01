from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[str] = None
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[int] = None
    endereco_cep: Optional[str] = None
    endereco_logradouro: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_uf: Optional[str] = None
    registro_profissional: Optional[bool] = None
