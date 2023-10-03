from command import Command
import discord
from data import Data

class HelpCmd(Command):

    @classmethod
    def help_text(cls) -> str | list[str]:
        return "help"

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) == 1

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        channel = message.channel
        await cls.pr_help(channel)

    @classmethod
    async def pr_help(cls, channel: discord.TextChannel):
            build="**Commands:**\n"
            for sc in Command.__subclasses__():
                sc: Command
                help_txt = sc.help_text()

                if not isinstance(help_txt, list):
                    help_txt = [help_txt]
                
                for i in help_txt:
                    build+="\- `{0}`\n".format(i)
                
            await channel.send(build.strip())