from fastapi import FastAPI
import httpx
from pydantic import BaseModel
from typing import Optional
from routers import anime


class Anime(BaseModel):
    name: str
    trailer: Optional[str]
    image: Optional[str]
    mal_id: int
    episodi: Optional[int]
    anno_uscita_fine: Optional[str]
    media_voto: float
    classifica: Optional[int]
    votato_da: Optional[int]
    sinopsi: Optional[str]
    background: Optional[str]
    genere_1: str
    genere_2: Optional[str]
    genere_3: Optional[str]
    studio: Optional[str]

