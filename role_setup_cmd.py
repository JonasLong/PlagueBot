import command
from data import Data
import discord
from infection import Infection

class RoleSetupCmd(command.Command):
    red = discord.Colour.from_str("#ff0000")
    yellow = discord.Colour.from_str("#F1C40F")
    green = discord.Colour.green()

    colors = [green, yellow, red]

    t=""":warning: Running this command will create 3 new hoisted and colored vanity roles named `Healthy`, `Infected`, and `Dead`.
If you already have roles you want to use for this purpose, rename your roles to the above names instead.
(Names are case-sensitive and should not be duplicated)

Are you sure you want to create new roles? If so, run this command again as `rolesetup confirm`"""

    @classmethod
    def help_text(cls) -> str | list[str]:
        return "rolesetup"

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) < 3

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        channel = message.channel
        guild: discord.Guild = message.guild

        if(not message.author.guild_permissions.administrator):
            await channel.send("Only an administrator can use this command!")
            return
        
        if(len(args)==1):
            await channel.send(cls.t)
        else:
            if(args[1]=="confrim"):
                await channel.send("confrim")

            elif(args[1]=="confirm"):
                for i in Infection.Status:
                    color: discord.Colour = cls.colors[i.value-1]
                    await guild.create_role(mentionable=False, name=i.name, reason="PlagueBot role setup", color=color, hoist=True)
                await channel.send("Roles created successfully!")

            else:
                await channel.send("Invalid argument")