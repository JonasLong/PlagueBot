import discord
from data import data

from prefix import prefix
from command import command

class cmd_handler:
    
    def __init__(self):
        self.data_handle = data()

    @property
    def prefix(self):
        return self.data_handle.get("prefix","!")

    def is_command(self, message) -> bool:
        if(message.content.startswith(self.prefix)):
            print("iscommand = true")
            return True
        return False
    
    def strip_prefix(self, message: str):
        return message.removeprefix(self.prefix)
    
    async def handle(self, message: discord.Message):
        cmd_txt = self.strip_prefix(message.content).strip()
        channel = message.channel
        parts = cmd_txt.split(" ")
        cmd_front = parts[0]
        if(len(parts)>1):
            args = parts[1:]
        else:
            args = []

        if(len(cmd_front)==0):
            print("not command")
            return

        print("command!")

        c: command = None

        match cmd_front:
            case "prefix":
                c=prefix
                
            case _:
                message.channel.send("Unknown command", cmd_front)
                return
            
        if(await c.check_args(args, channel)):
            await c.handle(args, self.data_handle, channel)
        