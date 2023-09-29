import command
from data import data
import discord

class prefix(command.command):
    
    @classmethod
    def help_text(cls) -> str:
        return "prefix <new prefix>"

    @classmethod
    def _check_argnum(cls, arglen: int) -> bool:
        return arglen < 2

    @classmethod
    async def handle(cls, args: list, data_handle: data, channel: discord.TextChannel):
        cur_prefix = data_handle.get("prefix", None)
        if(len(args)==0):
            await channel.send("Prefix is set to `{0}`".format(cur_prefix))
        
        else:
            pre = args[0]
            if(pre==cur_prefix):
                await channel.send("Prefix is already set to `{0}`".format(pre))
            else:
                print("changing prefix to {0}".format(pre))
                
                data_handle.set("prefix", pre)
                await channel.send("Changed prefix to `{0}`".format(pre))
