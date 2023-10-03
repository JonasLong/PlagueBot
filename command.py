from abc import ABC, abstractmethod
import discord
from data import Data

class Command(ABC):

    @classmethod
    @abstractmethod
    def help_text(cls) -> str | list[str]:
        pass

    @classmethod
    async def check_args(cls, args, channel: discord.TextChannel) -> bool:
        if(cls._validate_args(args)):
            return True
        else:
            await cls.send_help_msg(channel)
            return False

    @classmethod
    async def send_help_msg(cls, channel: discord.TextChannel):
        help_txt = cls.help_text()
        
        if isinstance(help_txt, list):
            build="Usage:"
            for i in help_txt:
                build+="\n`{0}`".format(i)
            await channel.send(build)
        else:
            await channel.send("Usage: `{0}`".format(help_txt))


    @classmethod
    @abstractmethod
    def _validate_args(cls, args: list) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        pass
    