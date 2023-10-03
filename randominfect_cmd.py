import command
from data import Data
import discord
from infection import Infection
import random

class RandomInfectCmd(command.Command):

    @classmethod
    def help_text(cls) -> str | list[str]:
        return "[randominfect] <num users>"

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) == 2

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        channel = message.channel
        
        try:
            numInfections = int(args[1])
        except ValueError:
            await channel.send("Invalid number to infect.")
            return

        if numInfections < 1:
            await channel.send("Invalid argument. Number to infect must be positive.")
        
        else:
            role: discord.Role = await Infection._get_status_role_for_guild(Infection.Status.Healthy, channel.guild)
            healthy: list[discord.Member] = role.members[:]
            for i in healthy:
                if i.bot:
                    healthy.remove(i)

            if(numInfections > len(healthy)):
                if(len(healthy)==0):
                    await channel.send("There are no healthy members. First run `heal` or `healall`.")
                else:
                    await channel.send("Number to infect is greater than the number of healthy members ({0}).".format(len(healthy)))


            else:
                random.shuffle(healthy)
                for i in range(numInfections):
                    await Infection.set_status(Infection.Status.Infected, healthy[i])

                if(numInfections>1):
                    msg = "{0} random users have been infected!".format(numInfections)
                else:
                    msg = "1 random user has been infected!"
                
                await channel.send(msg)
    
