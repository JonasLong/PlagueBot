import discord #pip install discord.py-self
import io
import time
from data import Data
from msg_handler import MsgHandler
from cmd_handler import CmdHandler

class PBClient(discord.Client):
    msg_handle: MsgHandler
    cmd_handle: CmdHandler

    async def on_ready(self):
        print('Logged in as', self.user)

    async def on_message(self, message: discord.Message):
        if(message.author!=self.user):
            if(self.cmd_handle.is_command(message)):
                print("new command:", message.content)
                await self.cmd_handle.handle(message)

            else:
                print("new message:", message.content)
                await self.msg_handle.handle(message)
        

intents = discord.Intents.default()
intents.message_content = True

client = PBClient(intents=intents)
client.msg_handle = MsgHandler()
client.cmd_handle = CmdHandler()
with open("data/key.txt") as key_file:
    api_key=key_file.readline()
assert (len(api_key)>0) #give error if no api key in the file
client.run(api_key)