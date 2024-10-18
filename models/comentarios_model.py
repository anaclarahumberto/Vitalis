from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Publicacao:
    id: Optional[str] = None
    descricao: Optional[str] = None
    id_usuario: Optional[str] = None
    