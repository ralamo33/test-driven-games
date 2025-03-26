from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os
from typing import Dict

from game_session import GameSession
from game.move import Move
app = FastAPI()

# Store active games in memory (in a real app, you'd use a database)
games: Dict[str, GameSession] = {}

# Mount the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/api/games")
async def create_game():
    game = GameSession()
    game_id = str(len(games) + 1)  # Simple ID generation
    games[game_id] = game
    return {
        "game_id": game_id,
        "board": game.display_htmx(),
        "turn": str(game.turn)
    }

@app.post("/api/games/{game_id}/move")
async def make_move(game_id: str, move: Move):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    try:
        game.move(move)
        
        return {
            "board": game.display_htmx(),
            "turn": str(game.turn),
            "is_over": game._is_over(),
            "winner": str(game.winner) if game._is_over() else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/games/{game_id}")
async def get_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    return {
        "board": game.display_htmx(),
        "turn": str(game.turn),
        "is_over": game._is_over(),
        "winner": str(game.winner) if game._is_over() else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 