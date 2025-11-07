from models.db_models import AnimeDB, AnimeCreate
from sqlalchemy.orm import Session

# --- GET anime dal DB per ID ---
def get_anime_by_id_db(anime_id: int, db: Session):
    return db.query(AnimeDB).filter(AnimeDB.mal_id == anime_id).first()

# --- AGGIUNGI anime al DB ---
def add_anime(anime: AnimeCreate, db: Session):
    try:
        existing = db.query(AnimeDB).filter(AnimeDB.mal_id == anime.mal_id).first()
        if existing:
            return {"message": "Anime già presente nel database."}

        db_anime = AnimeDB(
            mal_id=anime.mal_id,
            name=anime.name,
            trailer=anime.trailer,
            image=anime.image,
            episodi=anime.episodi,
            anno_uscita_fine=str(anime.anno_uscita_fine) if anime.anno_uscita_fine else None,
            media_voto=anime.media_voto,
            voto_personale=anime.voto_personale,
            visto_nonvisto=anime.visto_nonvisto,
            classifica=anime.classifica,
            votato_da=anime.votato_da,
            sinopsi=anime.sinopsi,
            background=anime.background,
            genere_1=anime.genere_1,
            genere_2=anime.genere_2,
            genere_3=anime.genere_3,
            studio=anime.studio
        )

        db.add(db_anime)
        db.commit()
        db.refresh(db_anime)
        return {"message": "Anime aggiunto con successo."}

    except Exception as e:
        db.rollback()
        return {"message": f"Errore durante l'aggiunta: {str(e)}"}

# --- RICERCA anime nel DB per ID o nome ---
def search_anime_db(query: str, db: Session):
    if query.isdigit():
        result = db.query(AnimeDB).filter(AnimeDB.mal_id == int(query)).all()
    else:
        result = db.query(AnimeDB).filter(AnimeDB.name.ilike(f"%{query}%")).all()
    return result

# --- DELETE anime dal DB ---
def delete_anime_db(mal_id: int, db: Session):
    anime = db.query(AnimeDB).filter(AnimeDB.mal_id == mal_id).first()
    if not anime:
        return {"message": "Anime non trovato."}
    db.delete(anime)
    db.commit()
    return {"message": f"Anime con mal_id={mal_id} cancellato con successo."}

# --- OTTIENI tutti gli anime ---
def get_all_anime(db: Session):
    return db.query(AnimeDB).order_by(AnimeDB.name).all()
