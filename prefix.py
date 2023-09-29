import command
from data import data
import discord

class prefix(command.command):
    
    @classmethod
    def help_text(cls) -> str:
        return "prefix <new prefix>"

    @classmethod
    def num_args(cls) -> int:
        return 1

    @classmethod
    def handle(cls, args: list, data_handle: data, channel: discord.TextChannel):
        pre = args[0]
        print("changing prefix to", pre)
        
        data_handle.set("prefix",pre)
        channel.
