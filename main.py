import discord
from discord.ext import commands
import yt_dlp
import random
import asyncio
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the Discord token from the environment variable
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

queue = []

@bot.event
async def on_ready():
    print(f"🎉 Logged in as {bot.user}")

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('title', 'Unknown'), "song.mp3"
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None, None

async def play_next(ctx):
    if queue:
        url = queue.pop(0)
        title, file_path = download_audio(url)
        
        if title is None or file_path is None:
            await ctx.send("❌ Error occurred while trying to download the song.")
            return
        
        source = discord.FFmpegPCMAudio(file_path)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f"🎶 Now playing: *{title}*")
    else:
        await ctx.send("🧘 Queue is empty. Use !mood to auto-play or !play to add songs.")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    if os.path.exists("song.mp3"):
        os.remove("song.mp3")

@bot.command()
async def play(ctx, url):
    queue.append(url)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)
    else:
        await ctx.send("✅ Added to queue.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipping...")

@bot.command()
async def stop(ctx):
    queue.clear()
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    await ctx.send("🛑 Stopped and cleared the queue.")

@bot.command()
async def nowplaying(ctx):
    await ctx.send("🎵 Currently playing whatever's loaded in FFmpeg. (This can be expanded with a real state tracker.)")

mood_songs = {
    "happy": [
        "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Happy - Pharrell Williams
        "https://www.youtube.com/watch?v=PT2_F-1esPk",  # Can't Stop the Feeling - Justin Timberlake
        "https://www.youtube.com/watch?v=3ywIuicGG64",  # Walking on Sunshine - Katrina & The Waves
        "https://www.youtube.com/watch?v=ykW4rtW2eu0"   # Don't Stop Me Now - Queen
    ],
    "sad": [
        "https://www.youtube.com/watch?v=RgKAFK5djSk",  # See You Again - Wiz Khalifa ft. Charlie Puth
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g",  # Someone Like You - Adele
        "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Shape of You - Ed Sheeran (acoustic sad version)
        "https://www.youtube.com/watch?v=njG7p6CSbCU"   # Everybody Hurts - R.E.M.
    ],
    "energetic": [
        "https://www.youtube.com/watch?v=kXYiU_JCYtU",  # Uptown Funk - Bruno Mars
        "https://www.youtube.com/watch?v=OPf0YbXqDm0",  # Mark Ronson - Uptown Funk ft. Bruno Mars
        "https://www.youtube.com/watch?v=h_D3VFfhvs4",  # Michael Jackson - Beat It
        "https://www.youtube.com/watch?v=fLexgOxsZu0"    # The Weeknd - Blinding Lights
    ],
    "relaxed": [
        "https://www.youtube.com/watch?v=7maJOI3QMu0",  # Bob Marley - Three Little Birds
        "https://www.youtube.com/watch?v=JGhoLcsr8GA",   # Jack Johnson - Banana Pancakes
        "https://www.youtube.com/watch?v=W8r-tXRLazs",   # Norah Jones - Don't Know Why
        "https://www.youtube.com/watch?v=5PSNL1qE6VY"    # Jason Mraz - I'm Yours
    ],
    "romantic": [
        "https://www.youtube.com/watch?v=YJVmu6yttiw",  # Ed Sheeran - Perfect
        "https://www.youtube.com/watch?v=YkgkThdzX-8",   # John Legend - All of Me
        "https://www.youtube.com/watch?v=WpYeekQkAdc",   # The Beatles - Something
        "https://www.youtube.com/watch?v=Y5fBdpreJiU"    # Elvis Presley - Can't Help Falling in Love
    ],
    "angry": [
        "https://www.youtube.com/watch?v=3JcmQONgXJM",   # Linkin Park - In the End
        "https://www.youtube.com/watch?v=B1zCN0YhW1s",   # Eminem - Lose Yourself
        "https://www.youtube.com/watch?v=8UVNT4wvIGY",    # Imagine Dragons - Believer
        "https://www.youtube.com/watch?v=3jWRrafhO7M"     # Rage Against the Machine - Killing in the Name
    ],
    "nostalgic": [
        "https://www.youtube.com/watch?v=9bZkp7q19f0",    # PSY - Gangnam Style
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",    # Rick Astley - Never Gonna Give You Up
        "https://www.youtube.com/watch?v=JGhoLcsr8GA",    # Jack Johnson - Banana Pancakes
        "https://www.youtube.com/watch?v=6Ejga4kJUts"     # Queen - Bohemian Rhapsody
    ],
    "workout": [
        "https://www.youtube.com/watch?v=3vtD3PqUHSg",    # Eye of the Tiger - Survivor
        "https://www.youtube.com/watch?v=ebXbLfLACGM",    # The Final Countdown - Europe
        "https://www.youtube.com/watch?v=btPJPFnesV4",    # Thunderstruck - AC/DC
        "https://www.youtube.com/watch?v=6Zbi0XmGtMw"     # Lose Yourself - Eminem
    ],
    "chill": [
        "https://www.youtube.com/watch?v=DohRa9lsx0Q",     # Coldplay - Strawberry Swing
        "https://www.youtube.com/watch?v=7wtfhZwyrcc",     # Imagine Dragons - Birds
        "https://www.youtube.com/watch?v=To7P6czurB4",     # Billie Eilish - Ocean Eyes
        "https://www.youtube.com/watch?v=GxBSyx85Kp8"      # Tame Impala - The Less I Know The Better
    ]
}


@bot.command()
async def mood(ctx, mood_type):
    mood_type = mood_type.lower()
    if mood_type in mood_songs:
        random_song = random.choice(mood_songs[mood_type])
        queue.append(random_song)
        await ctx.send(f"💽 Mood '{mood_type}' activated. Adding a random song...")
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await play_next(ctx)
    else:
        await ctx.send("❌ Unknown mood. Available: happy, sad, focus")

bot.run(DISCORD_TOKEN)