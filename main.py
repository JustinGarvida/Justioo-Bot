from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response


# Specify the path to the .env file
dotenv_path = "/Users/justingarvida/Projects/Justioo-Bot/venv/.env"
load_dotenv(dotenv_path)
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("Discord token not found in environment variables.")


#Make Bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


#Message Functionalities
async def send_message(message: Message, user_message: str) -> None:
   if not user_message:
       print("Message was empty bc intents were not handled properly.")
       return
   if is_private := user_message[0] == '?':
       user_message = user_message[1]
  
   try:
       response:str = get_response(user_message)
       await message.author.send(response) if is_private else await message.channel.send(response)
   except Exception as e:
       print(e)


#Handling Bot StartUp
@client.event
async def on_ready() -> None:
   print(f'{client.user} is now running!')


#Handing Incoming Messages
@client.event
async def on_message(message: Message) -> None:
   if message.author == client.user:
       return
   username: str = str(message.author)
   user_message: str = str(message.content)
   channel: str = str(message.channel)


   print(f'[{channel}] {user_message}: "{user_message}"')
   await send_message(message, user_message)


#entry point
def main() -> None:
   client.run(token=TOKEN)


if __name__ == "__main__":
   main()