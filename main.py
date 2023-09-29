import discord #pip install discord.py-self
import io
import time
from data import data
from msg_handler import msg_handler

class MyClient(discord.Client):
                
    async def on_ready(self):
        print('Logged in as', self.user)

    async def on_message(self, message):
        await handler.handle(message)
        

handler = msg_handler()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
with open("data/key.txt") as key_file:
    api_key=key_file.readline()
assert (len(api_key)>0) #give error if no api key in the file
client.run(api_key)