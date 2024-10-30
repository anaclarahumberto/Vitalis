from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioAutenticado:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    tipo_perfil: Optional[int] = None
    foto_perfil: Optional[bool] = None
    nome_perfil: Optional[str] = None
    bio_perfil: Optional[str] = None
    categoria_perfil: Optional[str] = None
    genero: Optional[str] = None
    tipo_paciente: Optional[int] = None