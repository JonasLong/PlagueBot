from enum import Enum
from data import Data
import discord
import random

class Infection:
    Status = Enum("Status", ["Healthy", "Infected", "Dead"])
    prop_names="healc,infc,deathc".split(",")
    default_c = .10

    corpse_transmission = True

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
        return None

    @classmethod
    async def role_setup(cls, guild: discord.Guild):
        #TODO
        pass

    @classmethod
    async def try_advance_infection(cls, target: discord.Member) -> Status | None:
        status = await cls.get_status(target)
        if status == cls.Status.Infected:
            r = random.random()
            print(r)
            heal_chance = cls.get_chance_from_status(cls.Status.Healthy)
            die_chance = cls.get_chance_from_status(cls.Status.Dead)

            if(r < heal_chance):
                await  cls.set_status(cls.Status.Healthy, target)
                return cls.Status.Healthy
            
            elif(r < heal_chance + die_chance):
                await cls.set_status(cls.Status.Dead, target)
                return cls.Status.Dead
            
        return None
    
    @classmethod
    async def try_pass_infection(cls, source: discord.Member, dest: discord.Member) -> bool:
        src_status = await cls.get_status(source)
        dst_status = await cls.get_status(dest)
        if(src_status == cls.Status.Infected or (cls.corpse_transmission and src_status == cls.Status.Dead)):
            if(dst_status == cls.Status.Healthy):
                r = random.random()
                inf_chance = cls.get_chance_from_status(cls.Status.Infected)
                if(r < inf_chance):
                    await cls.set_status(cls.Status.Infected, dest)
                    return True
        return False

    @classmethod
    def get_chance_from_status(cls, status: Status):
        return Data.get(cls.prop_names[status.value-1], cls.default_c)
    
    @classmethod
    def _set_chance_for_status(cls, status: Status, chance: float):
        return Data.set(cls.prop_names[status.value-1], chance)

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
    
    