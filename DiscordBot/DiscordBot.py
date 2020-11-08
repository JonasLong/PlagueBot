
# bot.py
import os
import discord
import json
import time

class ConfigFiles:
    curdir=os.path.curdir
    
    conf_file="config.json"
    inst_ids=[]
    inst_pointers=[]
    folders={"guild":"guildConfig"}

    @classmethod
    def get_inst(cls,folder_type,id):
        guildid=str(id)+folder_type
        if guildid in cls.inst_ids:
            return cls.inst_pointers[cls.inst_ids.index(guildid)]
        else:
            return ConfigFiles(id,folder_type)

    def __init__(self,id,folder_type):
        self.id=str(id)
        self.dict_loaded=False
        self.folder=os.path.join(ConfigFiles.curdir,ConfigFiles.folders[folder_type])
        assert not self.id+self.folder in ConfigFiles.inst_ids
        ConfigFiles.inst_ids.append(self.id+folder_type)
        ConfigFiles.inst_pointers.append(self)

    def __del__(self):
        #remove entry to allow creation of a new instance
        ConfigFiles.inst_ids.remove(self.id)
        ConfigFiles.inst_pointers.remove(self)

    def get_tag(self,tag,not_found={}):
        if not self.dict_loaded:
            self.load_dict()
        return self.dictionary.get(tag,not_found)

    def set_tag(self,tag,value):
        if not self.dict_loaded:
            self.load_dict()
        self.dictionary[tag]=value
        self.save_dict()

    def load_dict(self):
        self.dictionary=self._load_json(self.id,self.folder)
        self.dict_loaded=True

    def save_dict(self):
        #Save
        self._export_json(self.dictionary,self.id,self.folder)

    @classmethod
    def load_text(cls,filename):
        file_path=os.path.join(cls.curdir,filename)
        with open(file_path,"r") as file:
            res=file.readlines()
        return res

    @classmethod
    def _check_folder_exists(self,folder,sub_path):
        assert os.path.exists(folder)
        if not os.path.exists(sub_path):
            print("guild folder does not exist, creating",sub_path)
            os.mkdir(folder_path)

    @classmethod
    def _check_file_exists(cls,file_path):
        if not os.path.exists(file_path):
            with open(file_path,"w") as file_obj:
                json.dump({}, file_obj)
            print("Created file",file_path)

    @classmethod
    def _export_json(cls,data,id,folder):
        print("File write")
        folder_path=os.path.join(folder,id)
        file_path=os.path.join(folder_path,cls.conf_file)
        cls._check_folder_exists(folder,folder_path)

        with open(file_path,"w") as file:
            json.dump(data,file)

    def _load_json(cls,id,folder):
        print("File read")
        folder_path=os.path.join(folder,id)
        file_path=os.path.join(folder_path,cls.conf_file)
        cls._check_folder_exists(folder,folder_path)
        cls._check_file_exists(file_path)

        with open(file_path,"r") as file:
            conf_data=json.load(file)
        return conf_data

class Diseases:

    @classmethod
    async def handle_messages(cls,msg):

        cur_server_inst=msg.guild
        server_inst=ConfigFiles.get_inst("guild",cur_server_inst)
        server_inst.get_tag("diseases",[])

    @classmethod
    async def get_active_users(cls):
        pass

    @classmethod
    async def check_infections(cls,msg):
        #Infect people
        pass

class BotCommands:

    commands=["help","prefix","setrole","viewroles","heal","infect","kill"]

    @classmethod
    async def handle_message(cls,msg):
        is_cmd=await cls.try_run_as_command(msg)
        if not is_cmd:
            await Diseases.handle_messages(msg)

    @classmethod
    async def try_run_as_command(cls,msg):
        #Get an instance of the config for this guild
        conf=ConfigFiles.get_inst("guild",msg.guild)
        prefix=conf.get_tag("conf").get("pre","!")

        c=cls.is_command(msg,prefix)
        if c:
            #Run command
            await cls.interepret_command(msg,conf,prefix)
        return c

    @classmethod
    def is_command(cls,msg,prefix):
        text=msg.content
        if not text.startswith(prefix):
            return False
        print("message matches prefix:",prefix)
        text=text.replace(prefix,"",1)
        
        is_command=False
        for command in cls.commands:
            if text.startswith(command):
                is_command=True
                break
        return is_command

    @classmethod
    async def interepret_command(cls,msg,conf_inst,prefix):
        text=msg.content.lower().replace(prefix,"",1)

        if text=="help":
            command_str="__Commands__:\n```"
            for command in cls.commands:
                command_str+=command+'\n'
            command_str=command_str[:len(command_str)-1]
            command_str+="```"
            await BotActions.send_msg(command_str, msg.channel)

        elif text.startswith("prefix"):
            if text=="prefix":
                pre=conf_inst.get_tag("conf").get("pre","!")
                await BotActions.send_msg('My prefix is "'+pre+'".', msg.channel)
            if text.startswith("prefix "):
                if cls.is_admin(msg.author):
                    pre=text.replace("prefix ","",1)
                    if not " " in pre:
                        conf=conf_inst.get_tag("conf")
                        conf["pre"]=pre
                        conf_inst.set_tag("conf",conf)
                        await BotActions.send_msg('Prefix set to "'+pre+'".', msg.channel)
                    else:
                        await BotActions.send_msg('"'+pre+'" is not a valid prefix. Please restrict prefixes to 1 word.', msg.channel)
                else:
                    await cls.not_admin(msg.channel)
                
        elif text.startswith("setrole"):
            if cls.is_admin(msg.author):
                if text.startswith("setrole "):
                    if text.count(" ")>1:
                        parts=text.split(" ")
                        if parts[1] in ["healthy","infected","dead"]:
                            if len(msg.role_mentions)>0:
                                if len(msg.role_mentions)==1:
                                    #Command looks valid
                                    valid_statuses=["healthy","infected","dead"]
                                    health_status=valid_statuses.index(parts[1])
                                    rolename=msg.role_mentions[0]
                                    roles=conf_inst.get_tag("health_roles",[None,None,None])
                                    roles[health_status]=rolename.id
                                    conf_inst.set_tag("health_roles",roles)
                                    await BotActions.send_msg(parts[1]+' role has been set to '+rolename.mention, msg.channel)
                                else:
                                    await BotActions.send_msg('Too many role mentions at once, use 1 mention at a time', msg.channel)
                            else:
                                await BotActions.send_msg('Invalid mention, must mention a server role.', msg.channel)

                        else:
                            await BotActions.send_msg('"'+str(parts[1])+'" is not a valid parameter. Must use healthy/infected/dead.', msg.channel)
                    else:
                        await BotActions.send_msg('Wrong number of arguments', msg.channel)
                else:
                    if text=="setrole":
                        await BotActions.send_msg('Usage: `setrole healthy/infected/dead @roleName`\nUsers who have this health status will be given this role. Use `viewroles` to see what roles have been set.', msg.channel)
                    else:
                        await BotActions.send_msg('Invalid arguments for command `setrole`',msg.channel)
            else:
                await cls.not_admin(msg.channel)

        elif text.startswith("viewroles"):
            if cls.is_admin(msg.author):
                roles=conf_inst.get_tag("health_roles",[None,None,None])
                mentions=[]
                for role in roles:
                    id=roles[len(mentions)]
                    if id is None:
                        mentions.append("`No role assigned`")
                    else:
                        mentions.append(discord.utils.get(msg.guild.roles,id=id).mention)
                await BotActions.send_msg('__Roles__:\nHealthy: '+mentions[0]+'\nInfected: '+mentions[1]+'\nDead: '+mentions[2], msg.channel)
            else:
                await cls.not_admin(msg.channel)

        elif text.startswith("heal"):
            await cls.change_health_status(msg,text,conf_inst,"Heal",0)

        elif text.startswith("infect"):
            await cls.change_health_status(msg,text,conf_inst,"Infect",1)

        elif text.startswith("kill"):
            await cls.change_health_status(msg,text,conf_inst,"Kill",2)

        else:
            print('command "'+str(text)+'" not recognized')

    #ABSTRACTIONS

    @classmethod
    async def not_admin(cls,channel):
        await BotActions.send_msg("Sorry, only server administrators can use that command.",channel)

    @classmethod
    def is_admin(cls,author):
        return author.guild_permissions.administrator

    @classmethod
    async def change_health_status(cls,msg,text,conf_inst,statusname,statusnum):
        if cls.is_admin(msg.author):
            if text==statusname:
                    await BotActions.send_msg('__Usage__:\n`'+statusname+' @user` or '+statusname+' @user @user2 @user3`', msg.channel)
            else:
                if len(msg.mentions)>0:
                    #Get objects of the health status roles for this server
                    roles=conf_inst.get_tag("health_roles",[None,None,None])
                    err=False
                    role_objects=[]
                    for role_id in roles:
                        if not err:
                            if role_id is None:
                                err=True
                                await BotActions.send_msg('A role has not been set. Use `viewroles` to see all unset status roles.', msg.channel)
                            else:
                                role_objects.append(discord.utils.get(msg.guild.roles,id=role_id))
                    if not err:
                        #Save the role that should be added
                        role_to_add=role_objects[statusnum]
                        role_objects.pop(statusnum)
                        #Remove all roles (from all mentioned users) that are not the role to be added
                        for role_to_remove in role_objects:
                            for user_mention in msg.mentions:
                                await BotActions.remove_role(user_mention,role_to_remove)
                        #Give all mentioned users the role to add
                        for user_mention in msg.mentions:
                            await BotActions.add_role(user_mention,role_to_add)
                        #Report success
                        if len(msg.mentions)>1:
                            await BotActions.send_msg(statusname+'ed '+str(len(msg.mentions))+' users.', msg.channel)
                        else:
                            await BotActions.send_msg(statusname+'ed '+msg.mentions[0].mention+'.', msg.channel)
                else:
                    await BotActions.send_msg('Invalid number of arguments', msg.channel)
        else:
            await cls.not_admin(msg.channel)

class BotActions:

    #EVENTS

    @classmethod
    async def start(cls,client):
        print(f'{client.user} has connected to Discord!')
        print(cls.client.user, "is connected to the following guilds:")
        for guild in cls.client.guilds:
            print("\t"+guild.name,"(id:"+str(guild.id)+")")

        await cls.set_status("Plague INC", discord.Status.online)

        print("\nREADY\n")

    @classmethod
    async def join_event(cls,member):
        print("user",member,"joined guild")

    @classmethod
    async def message_event(cls,message):
        #message.content is the text of the message
        #message.channel is the channel
        if message.author == cls.client.user:
            print("message sent")
            return
        else:
            print("user",message.author,"sent message",message.content)
            await BotCommands.handle_message(message)
            #author=message.author
            #await cls.add_role(author,cls.role)


    #ACTIONS

    @classmethod
    async def add_role(cls,user,role):
        print("gave", user, "role", role)
        await user.add_roles(role)

    @classmethod
    async def remove_role(cls,user,role):
        print("removed", user, "role", role)
        await user.remove_roles(role)

    @classmethod
    async def send_msg(cls,message,channel):
        print('sent messge "'+message+'" in channel',channel)
        await channel.send(message)

    @classmethod
    async def send_dm(cls,msg,user):
        print("set dm", msg, "to", user)
        await user.create_dm()
        await user.dm_channel.send(msg)

    @classmethod
    async def set_status(cls,text,status):
        print("set own status to", text)
        await cls.client.change_presence(status=status, activity=discord.Game(text))
        

### MAIN ###

#becuase im too lazy to figure out the keystore
TOKEN=ConfigFiles.load_text("token.txt")[0]

print("CWD is",os.path.curdir)
print("Contents:",next(os.walk('.'))[1])

assert TOKEN!=None
client = discord.Client()
BotActions.client=client

@client.event
async def on_ready():
    await BotActions.start(client)

@client.event
async def on_member_join(member):
    await BotActions.join_event(member)

@client.event
async def on_message(message):
    await BotActions.message_event(message)
    
client.run(TOKEN)