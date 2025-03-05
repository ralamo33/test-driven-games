from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
from game import Game
from move import Move
from typing import Dict, Optional

app = FastAPI()

# Store active games in memory (in a real app, you'd use a database)
games: Dict[str, Game] = {}

class MoveRequest(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int

# Mount the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/api/games")
async def create_game():
    game = Game()
    game_id = str(len(games) + 1)  # Simple ID generation
    games[game_id] = game
    return JSONResponse({
        "game_id": game_id,
        "board": game._display(),
        "turn": str(game.turn)
    })

@app.post("/api/games/{game_id}/move")
async def make_move(game_id: str, move: MoveRequest):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    try:
        game.move(Move(
            from_row=move.from_row,
            from_col=move.from_col,
            to_row=move.to_row,
            to_col=move.to_col
        ))
        
        return JSONResponse({
            "board": game._display(),
            "turn": str(game.turn),
            "is_over": game._is_over(),
            "winner": str(game.winner) if game._is_over() else None
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/games/{game_id}")
async def get_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    return JSONResponse({
        "board": game._display(),
        "turn": str(game.turn),
        "is_over": game._is_over(),
        "winner": str(game.winner) if game._is_over() else None
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 