# 🎶 Riya Bot - Discord Music Bot

Riya Bot is a lightweight, easy-to-use Discord music bot built using Python and `discord.py`. It lets you play music from YouTube, queue up tracks, and even match songs to your mood.

## 💡 Features

* ✅ Join and leave voice channels
* 🔊 Play music from YouTube URLs
* 📃 Queue management (add, play, skip, stop)
* 🎭 Mood-based music selection (e.g., happy, sad, relaxed)
* 🎧 Auto play next song
* 🧽 Clean and efficient audio file handling

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* FFmpeg installed and added to PATH
* A bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/riya-bot.git
   cd riya-bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt`** :

   ```
   discord.py
   yt_dlp
   ```

3. **Set your bot token:**

   Open `main.py` and replace:

   ```python
   bot.run("YOUR_TOKEN_HERE")
   ```

4. **Run the bot:**

   ```bash
   python main.py
   ```

---

## 🛠 Commands

| Command        | Description                                |
| -------------- | ------------------------------------------ |
| `!join`        | Bot joins your current voice channel       |
| `!leave`       | Bot leaves the voice channel and cleans up |
| `!play <url>`  | Play a YouTube URL or add to queue         |
| `!skip`        | Skip the currently playing song            |
| `!stop`        | Stop playback and clear the queue          |
| `!nowplaying`  | Display the currently playing track        |
| `!mood <type>` | Play a song based on your mood (see below) |

### Supported Moods

`happy`, `sad`, `energetic`, `relaxed`, `romantic`, `angry`, `nostalgic`, `workout`, `chill`

Example:

```
!mood relaxed
```

---

## 📁 File Management

Riya Bot downloads audio as `song.mp3` and deletes it after playback. Ensure you have permission to write to the working directory.

---

## 📌 Notes

* Riya Bot only supports **one server voice channel at a time**.
* If the bot crashes during audio playback, delete `song.mp3` manually to avoid errors.
* Audio files are overwritten on each new song, keeping disk usage minimal.

---

## 🛡️ Security Warning

Your current bot token is **exposed**. Regenerate it in the Discord Developer Portal and **never share it publicly**.

---

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a PR to suggest improvements.

---

## 📜 License

MIT License

---

