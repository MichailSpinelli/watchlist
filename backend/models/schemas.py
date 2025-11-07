from pydantic import BaseModel
from typing import Optional

class AnimeCreate(BaseModel):
    mal_id: int
    name: str
    trailer: Optional[str] = None
    image: Optional[str] = None
    episodi: Optional[int] = None
    anno_uscita_fine: Optional[str] = None
    media_voto: float
    voto_personale: Optional[float] = None
    visto_nonvisto: Optional[bool] = None
    classifica: Optional[int] = None
    votato_da: Optional[int] = None
    sinopsi: Optional[str] = None
    background: Optional[str] = None
    genere_1: str
    genere_2: Optional[str] = None
    genere_3: Optional[str] = None
    studio: Optional[str] = None

class AnimeRead(AnimeCreate):
    """Schema per leggere un anime dal DB"""
    pass
