from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import Optional
from routers import anime
from models.pydantic_models import Anime

async def get_anime_by_id(id: int):
    url = f"https://api.jikan.moe/v4/anime/{id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        # Se la risposta è un errore, gestiscila
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Errore da Jikan API: {response.status_code}")

        data = response.json().get("data")
        if not data:
            raise HTTPException(status_code=404, detail="Anime non trovato nella risposta Jikan")

        generi = data.get("genres", [])
        studios = data.get("studios", [])

        anime = Anime(
            name=data.get("title"),
            mal_id=data.get("mal_id"),
            genere_1=generi[0]["name"] if generi else "Sconosciuto",
            genere_2=generi[1]["name"] if len(generi) > 1 else None,
            genere_3=generi[2]["name"] if len(generi) > 2 else None,
            trailer=data.get("trailer", {}).get("embed_url"),
            image=data.get("images", {}).get("jpg", {}).get("small_image_url"),
            episodi=data.get("episodes"),
            anno_uscita_fine=data.get("aired", {}).get("string"),
            media_voto=data.get("score"),
            classifica=data.get("rank"),
            votato_da=data.get("scored_by"),
            sinopsi=data.get("synopsis"),
            background=data.get("background"),
            studio=studios[0]["name"] if studios else None
        )

        return anime