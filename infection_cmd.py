import command
from data import Data
import discord
from infection import Infection

class InfectionCmd(command.Command):

    @classmethod
    def help_text(cls) -> str:
        return "[infect/kill/heal] <username>"

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        return len(args) < 3

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        channel = message.channel
        if(len(args)==1):
            target = message.author
        else:
            if(len(message.mentions)==0):
                if(len(message.raw_role_mentions)>0):
                    await channel.send("Invalid argument- cannot mention a role")
                else:
                    await channel.send("Invalid argument- must mention a user")
                return
            target=message.mentions[0]
        
        match args[0]:
            case "infect":
                status = Infection.Status.Infected
                msg_txt="infected"
            case "kill":
                status = Infection.Status.Dead
                msg_txt="killed"
            case "heal":
                status = Infection.Status.Healthy
                msg_txt="healed"

        if status == await Infection.get_status(target):
            await channel.send("{0} is already {1}.".format(target.mention, msg_txt))
        
        else:
            await Infection.set_status(status, target)
            await channel.send("{0} has been {1}!".format(target.mention, msg_txt))


    
        
    
