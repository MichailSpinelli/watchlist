from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# Modello SQLAlchemy (DB)
class AnimeDB(Base):
    __tablename__ = "anime"  # nome della tabella in minuscolo

    mal_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    trailer = Column(String(2048))
    image = Column(String(2048))
    episodi = Column(Integer)
    anno_uscita_fine = Column(String(255))
    media_voto = Column(Float, nullable=False)
    voto_personale = Column(Float)
    visto_nonvisto = Column(Boolean)
    classifica = Column(Integer)
    votato_da = Column(Integer)
    sinopsi = Column(Text)
    background = Column(Text)
    genere_1 = Column(String(255), nullable=False)
    genere_2 = Column(String(255))
    genere_3 = Column(String(255))
    studio = Column(String(255))

# Modello Pydantic (input/output API)
class AnimeCreate(BaseModel):
    mal_id: int
    name: str
    trailer: str | None = None
    image: str | None = None
    episodi: int | None = None
    anno_uscita_fine: int | None = None
    media_voto: float
    classifica: int | None = None
    votato_da: int | None = None
    sinopsi: str | None = None
    background: str | None = None
    genere_1: str
    genere_2: str | None = None
    genere_3: str | None = None
    studio: str | None = None
    voto_personale: float | None = None
    visto_nonvisto: bool | None = None
