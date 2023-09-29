from abc import ABC, abstractmethod
import discord
from data import data

class command(ABC):

    @classmethod
    @abstractmethod
    def help_text(cls) -> str:
        pass

    @classmethod
    async def check_args(cls, args, channel: discord.TextChannel) -> bool:
        if(cls._check_argnum(len(args))):
            return True
        else:
            await cls.send_help_msg(channel)
            return False

    @classmethod
    async def send_help_msg(cls, channel: discord.TextChannel):
        await channel.send("Usage: `"+cls.help_text()+"`")


    @classmethod
    @abstractmethod
    def _check_argnum(cls, arglen: int) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def handle(cls, args: list, data_handle: data, channel: discord.TextChannel):
        pass
    