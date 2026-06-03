from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__, static_folder="static", template_folder=".")
app.config["SECRET_KEY"] = "tictactoe-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

game = {
    "board": [""] * 9,
    "current_turn": "X",
    "winner": None,
    "players": {},   # sid -> "X" or "O"
    "connected": 0,
}

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],  
        [0,3,6],[1,4,7],[2,5,8],  
        [0,4,8],[2,4,6]           
    ]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], [a,b,c]
    if all(board):
        return "draw", []
    return None, []

def reset_game():
    game["board"] = [""] * 9
    game["current_turn"] = "X"
    game["winner"] = None

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@socketio.on("connect")
def on_connect():
    sid = socketio.server.manager.rooms.get("/", {})
    game["connected"] += 1

    if game["connected"] <= 2:
        symbol = "X" if len(game["players"]) == 0 else "O"
        
        taken = set(game["players"].values())
        if "X" not in taken:
            symbol = "X"
        elif "O" not in taken:
            symbol = "O"
        else:
            symbol = "spectator"
    else:
        symbol = "spectator"

    from flask import request
    game["players"][request.sid] = symbol

    emit("assigned", {
        "symbol": symbol,
        "board": game["board"],
        "current_turn": game["current_turn"],
        "winner": game["winner"],
        "players_connected": len([p for p in game["players"].values() if p in ("X","O")])
    })

    player_count = len([p for p in game["players"].values() if p in ("X","O")])
    emit("player_joined", {"players_connected": player_count, "symbol": symbol}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    from flask import request
    symbol = game["players"].pop(request.sid, None)
    game["connected"] = max(0, game["connected"] - 1)
    player_count = len([p for p in game["players"].values() if p in ("X","O")])
    emit("player_left", {"players_connected": player_count, "symbol": symbol}, broadcast=True)

@socketio.on("make_move")
def on_move(data):
    from flask import request
    index = data.get("index")
    player_symbol = game["players"].get(request.sid)

    if (player_symbol != game["current_turn"] or
        game["winner"] or
        not (0 <= index <= 8) or
        game["board"][index] != ""):
        return

    game["board"][index] = player_symbol
    winner, winning_cells = check_winner(game["board"])

    if winner:
        game["winner"] = winner
    else:
        game["current_turn"] = "O" if game["current_turn"] == "X" else "X"

    emit("game_update", {
        "board": game["board"],
        "current_turn": game["current_turn"],
        "winner": winner,
        "winning_cells": winning_cells,
        "last_move": index,
        "last_player": player_symbol,
    }, broadcast=True)

@socketio.on("reset_game")
def on_reset():
    reset_game()
    emit("game_update", {
        "board": game["board"],
        "current_turn": game["current_turn"],
        "winner": None,
        "winning_cells": [],
        "last_move": -1,
        "last_player": "",
    }, broadcast=True)

if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n{'='*45}")
    print(f"  🎮  Tic-Tac-Toe Server Running!")
    print(f"{'='*45}")
    print(f"  Local:   http://localhost:5000")
    print(f"  Network: http://{local_ip}:5000")
    print(f"\n  Share the Network URL with your friend!")
    print(f"  Both must be on the same Wi-Fi/network.")
    print(f"{'='*45}\n")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
