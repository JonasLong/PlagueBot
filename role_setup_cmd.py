import command
from data import Data
import discord
from infection import Infection

class RoleSetupCmd(command.Command):

    t="""Running this command will create 3 new vanity roles named `Healthy`, `Infected`, and `Dead`.
If you already have roles you want to use for this purpose, rename those roles to the above names.
(Names are case-sensitive and should not be duplicated)

Are you sure you want to create new roles? If so, run this command again as `rolesetup confirm`"""

    @classmethod
    def help_text(cls) -> str:
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
                    await guild.create_role(mentionable=False, name=i.name, reason="PlagueBot role setup")

            else:
                await channel.send("Invalid argument")