from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from services import db_services
from connect_db import SessionLocal
from models.db_models import AnimeDB, AnimeCreate

router = APIRouter()

# Dependency per il DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AGGIUNGI anime ---
@router.post("/")
async def add_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    result = db_services.add_anime(anime, db)
    return result

# --- RICERCA anime ---
@router.get("/search")
async def search_anime(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    result = db_services.search_anime_db(query, db)
    return result

# --- DELETE anime dal DB ---
@router.delete("/{mal_id}")
async def delete_anime(mal_id: int, db: Session = Depends(get_db)):
    anime = db.query(AnimeDB).filter(AnimeDB.mal_id == mal_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime non trovato")
    db.delete(anime)
    db.commit()
    return {"message": f"Anime con mal_id={mal_id} cancellato con successo"}

# --- OTTIENI tutti gli anime ---
@router.get("/all")
async def get_all_anime(db: Session = Depends(get_db)):
    result = db_services.get_all_anime(db)
    return result
