from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

game = Game()
app = FastAPI()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start():
    game.start()


@app.get("/is_game_won")
async def is_game_won():
    return game.is_game_won()


@app.post("/move_column")
async def move_column(src, dst):
    return game.move_column(src, dst)


@app.post("/move_to_free")
async def move_to_free(src):
    return game.move_to_free(src)


@app.post("/move_from_free")
async def move_from_free(src, dst):
    return game.move_from_free(src, dst)


@app.post("/column_to_home")
async def column_to_home(src):
    return game.column_to_home(src)


@app.post("/free_to_home")
async def free_to_home(src):
    return game.free_to_home(src)


@app.get("/computer_play")
async def computer_play(sim):
    return game.computer_play(sim)


@app.post("/apply_move")
async def apply_move(game_instance, move):
    game.apply_move(game_instance, move)


@app.post("/undo")
async def undo():
    game.undo()
