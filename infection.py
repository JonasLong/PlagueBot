from enum import Enum
import discord

class Infection:
    Status = Enum("Status", ["Healthy", "Infected", "Dead"])

    @classmethod
    async def set_status(cls, new_status: Status, member: discord.Member):
        for status in cls.Status:
            role = await cls._get_status_role_for_guild(status, member.guild)
            if(role is None):
                print("Cannot find a role matching {0}!".format(status.name))
            else:
                if(role.name==new_status.name):
                    await cls._apply_role(member, role)
                else:
                    await cls._clear_role(member, role)

    @classmethod
    async def get_status(cls, member: discord.Member) -> Status:
        for status in cls.Status:
            role = await cls._get_status_role_for_member(status, member)
            if(not role is None):
                return status
        return cls.Status.Healthy #default to healthy

    @classmethod
    async def role_setup(cls, guild: discord.Guild):
        #TODO
        pass
    
    @classmethod
    async def _get_status_role_for_member(cls, status: Status, member: discord.Member) -> discord.Role | None:
        return discord.utils.get(member.roles, name=status.name)

    @classmethod
    async def _get_status_role_for_guild(cls, status: Status, guild: discord.Guild) -> discord.Role | None:
        return discord.utils.get(guild.roles, name=status.name) #todo categorize by role ID

    @classmethod
    async def _apply_role(cls, member: discord.Member, role: discord.role):
        #TODO check perms
        await member.add_roles(role)

    @classmethod
    async def _clear_role(cls, member: discord.Member, role: discord.role):
        await member.remove_roles(role)
    
    @classmethod
    async def _has_role(cls, member: discord.Member, role: discord.role) -> bool:
        return await role in member.roles
    
    