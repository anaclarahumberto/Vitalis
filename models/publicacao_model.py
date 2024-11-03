from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Publicacao:
    id: Optional[int] = None
    descricao: Optional[str] = None
    imagem: Optional[str] = None
    id_usuario: Optional[str] = None
    data_criacao: Optional[date] = None 
    curtidas: Optional[int] = None 
    comentarios: Optional[int] = None 
    