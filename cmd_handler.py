import discord
from data import Data

from prefix import Prefix
from command import Command
from help_cmd import HelpCmd
from infection_cmd import InfectionCmd
from statistics_cmd import StatisticsCmd
from role_setup_cmd import RoleSetupCmd

class CmdHandler:
    
    def __init__(self):
        self.data_handle = Data()

    @property
    def prefix(self):
        return self.data_handle.get("prefix","!")

    def is_command(self, message) -> bool:
        if(message.content.startswith(self.prefix)):
            #print("iscommand = true")
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

        c: Command = None

        match cmd_txt:
            case "help" | "helo":
                c=HelpCmd
            case "prefix":
                c=Prefix
            case "kill" | "heal" | "infect":
                c=InfectionCmd
            case "rolesetup": # | "setrole" | "viewroles":
                c=RoleSetupCmd
            case "stats" | "healc" | "infc" | "deathc":
                c=StatisticsCmd
            case _:
                await message.channel.send("Unknown command \"{0}\". Try `help` for a list of commands".format(discord.utils.escape_mentions(cmd_txt)))
                return
            
        if(await c.check_args(args, channel)):
            await c.handle(args, self.data_handle, message)