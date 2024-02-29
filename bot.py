from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from responses import get_response
import pymongo
from pymongo import MongoClient


# Specify the path to the .env file
dotenv_path = "/Users/justingarvida/Projects/Justioo-Bot/venv/.env"
load_dotenv(dotenv_path)
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("Discord token not found in environment variables.")


# Make Bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Make MongoDB Connection
mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")
print(f'{mongo_uri}')
cluster = MongoClient(mongo_uri)
db = cluster["discord_users"]
collection = db["user_info"]

# Message Functionalities
async def send_message(message: Message, user_message: str) -> None:
    if not user_message.strip():  # Check if message content is empty or contains only whitespace
        print("Message was empty because intents were not handled properly.")
        return
    if user_message.startswith('?'):  # Check if message is intended to be private
        user_message = user_message[1:]
    try:
        response = get_response(user_message)
        if response:  # Check if response is not empty
            await message.author.send(response) if message.guild is None else await message.channel.send(response)
    except Exception as e:
        print(e)


# Handling Bot StartUp
@client.event
async def on_ready() -> None:
    print(f'{client.user} has Connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Justio's Balls"))

# Handling Incoming Messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    print(f'[{message.channel}] {message.username}: "{message.user_message}"')
    await send_message(message, user_message)

# Entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
