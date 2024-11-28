from dataclasses import dataclass
from typing import Optional


@dataclass
class Seguidor:
    id_usuario_seguidor: Optional[int] = None
    id_usuario_seguindo: Optional[int] = None
    
    
    
