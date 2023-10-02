import discord
import time
import datetime
from infection import Infection
from data import Data

class MsgHandler:
    messages: dict = dict()

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

        if(len(msgs) > 0):
            last: discord.Message = msgs[-1]
            other_member = last.author
            if(other_member!=target_member):
                print("New message from {0} -> {1}".format(other_member, target_member))

                res = await Infection.try_pass_infection(other_member, target_member)
                if(res):
                    channel.send("{0} has passed their infection to {1}".format(other_member.mention, target_member.mention))
                
            else:
                print("Repeat message by {0}".format(last.author))

        new_status = await Infection.try_advance_infection(target_member)
        if(new_status == Infection.Status.Healthy):
            await channel.send("{0} has recovered from the plague :pray:".format(target_member.mention))
        elif(new_status == Infection.Status.Dead):
            await channel.send("{0} has died from the plague :skull:".format(target_member.mention))

        msgs.append(message)
        
    def _prune_msgs(self, msgs: list):
        if(len(msgs) > 0):
            #print("pruning msgs from this channel...")
            for i in msgs:
                i: discord.Message
                age: datetime.timedelta = datetime.datetime.now(datetime.timezone.utc) - i.created_at
                if age.total_seconds() > 10:
                    #print("message is {0}s old, pruning".format(age.total_seconds()))
                    msgs.remove(i)
                else:
                    #print("message within time to live ({0}s), ending pruning".format(age.total_seconds()))
                    return
            #print("all messages were pruned")


        
