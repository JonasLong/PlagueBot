import discord
from data import data

from prefix import prefix
from command import command
from infection_cmd import infection_cmd

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
        channel = message.channel
        args = self.strip_prefix(message.content).strip().split(" ")
        cmd_txt = args[0]

        if(len(cmd_txt)==0):
            print("not command")
            return

        print("command!")

        c: command = None

        match cmd_txt:
            case "prefix":
                c=prefix
            case "kill" | "heal" | "infect":
                c=infection_cmd
            case "updateroles":
                pass
            case _:
                await message.channel.send("Unknown command \"{0}\"".format(cmd_txt))
                return
            
        if(await c.check_args(args, channel)):
            await c.handle(args, self.data_handle, message)
        