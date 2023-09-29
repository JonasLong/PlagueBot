import discord
from data import data
from cmd_handler import cmd_handler

class msg_handler:
    cmd_handle: cmd_handler = cmd_handler()

    def __init__(self):
        pass

    async def handle(self, message: discord.Message):
        if(message.author!=discord.user):
            print("new message:",message.content)
            if(self.cmd_handle.is_command(message)):
                await self.cmd_handle.handle(message)