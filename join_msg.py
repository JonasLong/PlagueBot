import discord
from data import Data

class JoinMessager:
    target_channel_names = ["bot","command","general"]
    join_text = """:biohazard: **Thanks for using PlagueBot!** :biohazard:

For a list of commands, run `!help`.
Inital setup requires creating `Healthy`, `Infected`, and `Dead` roles. This can be done automatically with `!rolesetup`.
These roles will be auto-assigned to users by PlagueBot, so you can create channels exclusive to each role."""

    @classmethod
    async def check_guilds(cls, client: discord.Client):
        known_guilds: list = Data.get("guilds", [])
        new = False
        for g in client.guilds:
            if(not g.id in known_guilds):
                await cls.message(client, g)
                known_guilds.append(g.id)
                new = True
        
        if new:
            Data.set("guilds", known_guilds)

    @classmethod
    async def message(cls, client: discord.Client, guild: discord.Guild):
        c = await cls.get_target_channel(client, guild)
        if c is not None:
            await c.send(cls.join_text)
        else:
            print("Could not send join message in any channel")
        
    @classmethod
    async def get_target_channel(cls, client: discord.Client, guild: discord.Guild) -> discord.TextChannel | None:
        channels=guild.text_channels
        channels_copy = channels[:]
        for c in channels:
            if(not await cls.has_perms(client, c)):
                channels_copy.remove(c) #TODO check if this is valid in the for loop
            else:
                if await cls.is_ideal(c.name):
                    return c
                
        if len(channels)==0:
            return None
        return channels_copy[0]

    @classmethod
    async def is_ideal(cls, channel_name: str):
        for i in cls.target_channel_names:
            if i in channel_name:
                return True
        return False
    
    @classmethod
    async def has_perms(cls, client: discord.Client, channel: discord.TextChannel):
        return channel.permissions_for(channel.guild.get_member(client.user.id)).send_messages