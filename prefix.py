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
    async def handle(cls, args: list, data_handle: data, channel: discord.TextChannel):
        pre = args[0]
        if(pre==data_handle.get("prefix", None)):
            await channel.send("Prefix is already set to `{0}`".format(pre))
            return
        
        print("changing prefix to {0}".format(pre))
        
        data_handle.set("prefix", pre)
        await channel.send("Changed prefix to `{0}`".format(pre))
