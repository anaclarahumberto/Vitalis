from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioAutenticado:    
    nome: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[int] = None