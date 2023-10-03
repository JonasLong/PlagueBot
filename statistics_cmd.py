import discord
import command
from data import Data
from infection import Infection

class StatisticsCmd(command.Command):
    pstrs = ["Heal chance","Infection chance","Death chance"]

    @classmethod
    def help_text(cls) -> str | list[str]:
        return ["stats", "[healc/infc/deathc] <new probability>"]

    @classmethod
    def _validate_args(cls, args: list) -> bool:
        if(args[0]=="stats"):
            return len(args) == 1
        else:
            return len(args) < 3

    @classmethod
    async def handle(cls, args: list, data_handle: Data, message: discord.Message):
        chances=[]
        for i in Infection.prop_names:
            chances.append(data_handle.get(i, Infection.default_c))

        if args[0] == "stats":
                build=""
                for index, item in enumerate(cls.pstrs):
                    build+="{0}: `{1}`\n".format(cls.pstrs[index], chances[index])
                build=build.strip()
                await message.channel.send("**Stats:**\n"+build)
        else:
            pos = Infection.prop_names.index(args[0])

            if(len(args) == 1):
                await message.channel.send("{0}: `{1}`".format(cls.pstrs[pos], chances[pos]))
            else:
                args[1]=discord.utils.escape_markdown(discord.utils.escape_mentions(args[1]))
                try:
                    nval = float(args[1])
                except ValueError:
                    await message.channel.send("Invalid value \"{0}\". Argument must be a decimal value.".format(args[1]))
                    return

                if(nval>1 or nval<0):
                    await message.channel.send("Invalid value `{0}`. Argument must be between 0 and 1.".format(nval))

                else:
                    chances[pos] = nval

                    healc = chances[Infection.Status.Healthy.value-1]
                    deathc = chances[Infection.Status.Dead.value-1]

                    if healc + deathc > 1:
                        await message.channel.send("Invalid value `{0}`. Death chance and heal chance may not sum to more than `1.0`.".format(nval))
                    else:
                        #save values
                        for index, val_name in enumerate(Infection.prop_names):
                            data_handle.set(val_name, chances[index])
                        
                        await message.channel.send("{0} set to `{1}`".format(cls.pstrs[pos], chances[pos]))


        
