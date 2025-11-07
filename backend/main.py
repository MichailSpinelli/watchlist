from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import anime

app = FastAPI(
    title="Anime Watchlist API",
    description="API per ricerca anime su Jikan e gestione watchlist personale",
    version="1.0.0"
)

# -------------------------------
# Configurazione CORS (per frontend)
# -------------------------------
origins = [
    "http://localhost:5173",  # Vue.js dev server
    "http://localhost:8000",  # per test diretto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Includi il router anime
# -------------------------------
app.include_router(anime.router, prefix="/anime", tags=["Anime"])
