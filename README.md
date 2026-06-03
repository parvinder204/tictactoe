# 🎮 Multiplayer Tic-Tac-Toe (LAN Game)

A real-time multiplayer Tic-Tac-Toe game built with **Python**, **Flask**, and **Flask-SocketIO**.

Play against a friend on the **same Wi-Fi/LAN network** directly from your browser—no installation required for the second player.

---

## 🚀 Features

- 🟥 **X vs 🟩 O** — players are automatically assigned symbols
- ⚡ **Real-time gameplay** using WebSockets
- 🏆 **Winning cells are highlighted**
- 📊 **Live score tracker**
  - X Wins
  - Draws
  - O Wins
- 🔄 **New Game** button resets the board for both players simultaneously
- 👀 **Live turn indicator**
- 🔌 **Graceful disconnect handling**
- 🌐 Play from any device connected to the same network

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-SocketIO

### Frontend
- HTML
- CSS
- JavaScript

### Communication
- WebSockets (Socket.IO)


## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/parvinder204/tictactoe.git
cd tic-tac-toe
```

Install dependencies:

```bash
pip install flask flask-socketio
```

---

## ▶️ Running the Game

Start the server:

```bash
python server.py
```

When the server starts, you should see output similar to:

```text
Local:   http://localhost:5000
Network: http://192.168.1.42:5000
```

### Player 1

Open:

```text
http://localhost:5000
```

### Player 2

Open the **Network URL**:

```text
http://192.168.1.42:5000
```

> Both players must be connected to the same Wi-Fi or local network.

That's it—start playing! 🎉

---

## 🎯 How It Works

1. The first player to connect is assigned **X**.
2. The second player is assigned **O**.
3. Players take turns making moves.
4. The server synchronizes the game state in real time.
5. When a player wins:
   - Winning cells are highlighted
   - Scores are updated automatically
6. Players can start a new round using the **New Game** button.

---

## 📊 Score Tracking

The game keeps track of:

- X Wins
- Draws
- O Wins

Scores persist across rounds until the server is restarted.

---

## 🔌 Disconnect Handling

If a player disconnects:

- The remaining player is notified.
- The game state is handled gracefully.
- A new player can join when a slot becomes available.

---

## 🌐 Network Requirements

- Both devices must be connected to the same Wi-Fi or LAN.
- Ensure port **5000** is allowed through your firewall.
- Use the displayed **Network URL** to connect from another device.

---

## 🔮 Future Enhancements

- Room codes
- Player names
- In-game chat
- Spectator mode
- Mobile-friendly UI
- Sound effects
- Match history
- AI opponent mode
- Multiple game rooms

---
