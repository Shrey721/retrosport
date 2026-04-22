
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import os

app = FastAPI()

# Allow CORS for frontend development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for demo
players_db = [
    {
        "id": 1,
        "name": "John Doe",
        "position": "Forward",
        "stats": {"games": 20, "goals": 15, "assists": 5, "minutes": 1800}
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "position": "Midfielder",
        "stats": {"games": 22, "goals": 7, "assists": 12, "minutes": 2000}
    }
]

class Player(BaseModel):
    id: int
    name: str
    position: str
    stats: Dict[str, Any]

class AIQuery(BaseModel):
    question: str

@app.get("/api/players", response_model=List[Player])
def list_players():
    return players_db

@app.get("/api/players/{player_id}", response_model=Player)
def get_player(player_id: int):
    for player in players_db:
        if player["id"] == player_id:
            return player
    raise HTTPException(status_code=404, detail="Player not found")

@app.post("/api/players/{player_id}/ai")
def ai_assistant(player_id: int, query: AIQuery):
    player = next((p for p in players_db if p["id"] == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return {
        "answer": f"You asked: '{query.question}'. Here are {player['name']}'s stats: {player['stats']}"
    }

# Serve static frontend
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

# Optional: fallback to index.html for SPA routing
@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Not found")
