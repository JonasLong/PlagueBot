import command
from data import data
import discord

class prefix(command.command):
    
    @classmethod
    def help_text(cls) -> str:
        return "prefix <new prefix>"

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) < 3

    @classmethod
    async def handle(cls, args: list, data_handle: data, message: discord.Message):
        cur_prefix = data_handle.get("prefix", None)
        channel=message.channel
        if(len(args)==1):
            await channel.send("Prefix is set to `{0}`".format(cur_prefix))
        
        else:
            pre = discord.utils.escape_mentions(args[1])
            if(pre==cur_prefix):
                await channel.send("Prefix is already set to `{0}`".format(pre))
            else:
                print("changing prefix to {0}".format(pre))
                
                data_handle.set("prefix", pre)
                await channel.send("Changed prefix to `{0}`".format(pre))
