import command
from data import Data
import discord
from infection import Infection

class InfectAllCmd(command.Command):

    @classmethod
    def help_text(cls) -> str | list[str]:
        return ["[infectall/healall/killall]"]

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) == 1

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        channel = message.channel
        
        if(not message.author.guild_permissions.administrator):
            await channel.send("Only an administrator can use this command!")
            return

        match args[0]:
            case "infectall":
                status = Infection.Status.Infected
                msg_txt="infected"
            case "killall":
                status = Infection.Status.Dead
                msg_txt="killed"
            case "healall":
                status = Infection.Status.Healthy
                msg_txt="healed"

        await channel.send("Healing all server members...\nPlease wait, this could take a little while")
        num_updated = 0
        async for m in message.guild.fetch_members():
            if(await Infection.get_status(m)!=status and not m.bot):
                await Infection.set_status(status, m)
                num_updated+=1
        if(num_updated==0):
            await channel.send("All members are already {0}.".format(msg_txt))
        else:
            await channel.send("All members have been {0} ({1})!".format(msg_txt, num_updated))
        
    
