import discord
import time
import datetime
from infection import Infection
from data import Data

class MsgHandler:
    messages: dict = dict()
    default_msg_ttl_secs = 45

    def __init__(self):
        pass

    async def handle(self, message: discord.Message):
        channel = message.channel
        target_member = message.author
        msgs: list = self.messages.get(channel, None)

        if(msgs is None):
            msgs = []
            self.messages[channel] = msgs
        
        self._prune_msgs(msgs)
        print("{0} messages remaining after pruing".format(len(msgs)))

        if(len(msgs) > 0):
            last: discord.Message = msgs[-1]
            for msg in msgs:
                other_member = msg.author
                if(other_member!=target_member):
                    print("Attempting infection for {0} -> {1}".format(other_member, target_member))

                    res = await Infection.try_pass_infection(other_member, target_member)
                    if(res):
                        print("{0} infected by {1}".format(target_member.name, other_member.name))
                        await channel.send(":biohazard: {0} has passed their infection to {1} :biohazard:".format(other_member.mention, target_member.mention))
                        return
                
            print("{0} not infected by message".format(target_member))

        new_status = await Infection.try_advance_infection(target_member)
        if(new_status == Infection.Status.Healthy):
            await channel.send("{0} has recovered from the plague :pray:".format(target_member.mention))
        elif(new_status == Infection.Status.Dead):
            await channel.send("{0} has died from the plague :skull:".format(target_member.mention))

        msgs.append(message)
        
    def _prune_msgs(self, msgs: list):
        ttl: int = Data.get("msg_ttl_secs", self.default_msg_ttl_secs)
        prune=[]
        if(len(msgs) > 0):
            print("pruning msgs from this channel...")
            for i in msgs:
                i: discord.Message
                age: datetime.timedelta = datetime.datetime.now(datetime.timezone.utc) - i.created_at
                if age.total_seconds() > ttl:
                    print("message is {0}s old, pruning".format(age.total_seconds()))
                    prune.append(i)
                else:
                    print("message within time to live ({0}s), ending pruning".format(age.total_seconds()))
                    break

            for i in prune:
                msgs.remove(i)
            if(len(msgs)==0):
                print("all messages were pruned")


        
