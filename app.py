from fastapi import FastAPI
from fastapi.responses import FileResponse
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


# New endpoint to get the current game state
@app.get("/get_game_state")
async def get_game_state_api():
    """
    Returns the current state of the game board, including table, free cells, and home cells.
    """
    return {"table": game.table, "free": game.free, "home": game.home}


@app.post("/start")
async def start():
    """
    Starts a new FreeCell game.
    """
    game.start()
    # No return value needed, as the frontend will call get_game_state to refresh


@app.get("/is_game_won")
async def is_game_won():
    """
    Checks if the current game has been won.
    """
    return game.is_game_won()


@app.post("/move_column")
async def move_column(src: int, dst: int):
    """
    Moves a card from a source column to a destination column.
    Args:
        src (int): The index of the source column (0-7).
        dst (int): The index of the destination column (0-7).
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    return game.move_column(src, dst)


@app.post("/move_to_free")
async def move_to_free(src: int):
    """
    Moves a card from a column to a FreeCell.
    Args:
        src (int): The index of the source column (0-7).
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    return game.move_to_free(src)


@app.post("/move_from_free")
async def move_from_free(src: int, dst: int):
    """
    Moves a card from a FreeCell to a column.
    Args:
        src (int): The index of the source FreeCell (0-3).
        dst (int): The index of the destination column (0-7).
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    return game.move_from_free(src, dst)


@app.post("/column_to_home")
async def column_to_home(src: int):
    """
    Moves a card from a column to its appropriate HomeCell.
    Args:
        src (int): The index of the source column (0-7).
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    return game.column_to_home(src)


@app.post("/free_to_home")
async def free_to_home(src: int):
    """
    Moves a card from a FreeCell to its appropriate HomeCell.
    Args:
        src (int): The index of the source FreeCell (0-3).
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    return game.free_to_home(src)


@app.get("/computer_play")
async def computer_play(sim: int = 100):
    """
    Instructs the computer to make a move using MCTS.
    Args:
        sim (int): Number of simulations for the Monte Carlo Tree Search.
    Returns:
        tuple or None: The best move found (e.g., ('column_to_column', src, dst)) or None if no move found.
    """
    # The computer_play method in main.py already applies the move internally
    # So we just need to call it and return its result (the move made or None)
    return game.computer_play(sim)


@app.post("/undo")
async def undo():
    """
    Undoes the last game move.
    Returns:
        bool: True if undo was successful, False otherwise.
    """
    return game.undo()
